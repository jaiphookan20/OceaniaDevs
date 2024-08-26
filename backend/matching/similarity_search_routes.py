from datetime import time
from flask import Flask, request, jsonify, Blueprint, current_app, Response, stream_with_context
from models import Job, Candidate
from extensions import db
import numpy as np
from flask_cors import CORS
from utils.openai import get_embedding
from matching.similarity_search_service import SimilaritySearch
import time as python_time  # Rename the import to avoid confusion
import json

simsearch_blueprint = Blueprint('simsearch', __name__)
CORS(simsearch_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost:3000'}})
    
@simsearch_blueprint.route('/api/add_candidates_bulk', methods=['POST'])
def add_candidates_bulk():
    data = request.get_json()
    candidates = data['candidates']
    
    for candidate_data in candidates:
        # Extract candidate information from the request data
        name = candidate_data['name']
        years_experience = candidate_data['years_experience']
        position = candidate_data['position']
        work_experience = candidate_data['work_experience']
        favorite_languages = candidate_data['favorite_languages']
        technologies = candidate_data['technologies']
        
        # Combine all candidate details into a single text string
        candidate_text = f"{name} {position} {work_experience} {years_experience} {' '.join(favorite_languages)} {' '.join(technologies)}"

        # Generate embedding from the combined text
        embedding = get_embedding(candidate_text)
        
        # Convert numpy array to list if necessary
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        
        # Ensure the embedding is the correct length (1536 for OpenAI's embeddings)
        if len(embedding) != 1536:
            return jsonify({'status': 'error', 'message': f'Invalid embedding dimension for {name}'}), 400

        # Create a new Candidate object and add it to the database session
        candidate = Candidate(
            name=name,
            years_experience=years_experience,
            position=position,
            work_experience=work_experience,
            favorite_languages=favorite_languages,
            technologies=technologies,
            embedding=embedding
        )
        db.session.add(candidate)

    try:
        # Commit all changes to the database
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Candidates added successfully'}), 200
    except Exception as e:
        # If an error occurs, rollback the session and return an error message
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@simsearch_blueprint.route('/api/generate_job_embedding/<int:job_id>', methods=['POST'])
def generate_job_embedding_route(job_id):
    """
    Endpoint to generate and store an embedding for a specific job
    """
    sim_search_service = SimilaritySearch()
    embedding = sim_search_service.generate_job_embedding(job_id)
    if embedding:
        return jsonify({'status': 'success', 'message': 'Job embedding generated successfully'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Job not found'}), 404
    

@simsearch_blueprint.route('/api/get_matching_candidates/<int:job_id>', methods=['GET'])
def get_matching_candidates_route(job_id):
    """
    Endpoint to find and return candidates matching a specific job.
    """
    sim_search_service = SimilaritySearch()
    candidates = sim_search_service.find_matching_candidates(job_id)
    if candidates is None:
        return jsonify({'status': 'error', 'message': 'Job not found or embedding not generated'}), 404
    
    # Format the results to include only necessary information
    results = [{
        'candidate_id': c['candidate_id'],
        'name': c['name'],
        'position': c['position'],
        'years_experience': c['years_experience'],
        'work_experience': c['work_experience'],
        'favorite_languages': c['favorite_languages'],
        'technologies': c['technologies']
    } for c in candidates]
    
    return jsonify({'status': 'success', 'matches': results}), 200

# @simsearch_blueprint.route('/api/get_matching_candidates_with_explanation/<int:job_id>', methods=['GET'])
# def get_matching_candidates_with_explanation_route(job_id):
#     sim_search_service = SimilaritySearch()
#     candidates = sim_search_service.find_matching_candidates(job_id)
#     if candidates is None:
#         return jsonify({'status': 'error', 'message': 'Job not found or embedding not generated'}), 404

#     job = Job.query.get(job_id)
#     job_text = f"{job.title} {job.description} {job.specialization} {' '.join(job.tech_stack)}"

#     results = []
#     for candidate in candidates:
#         candidate_text = f"{candidate['position']} {candidate['work_experience']} {' '.join(candidate['favorite_languages'])} {' '.join(candidate['technologies'])}"
#         explanation = sim_search_service.generate_explanation(job_text, candidate_text)
        
#         if 'error' in explanation:
#             current_app.logger.error(f"Error generating explanation for candidate {candidate['candidate_id']}: {explanation['error']}")
#             explanation = {'match_explanation': 'Unable to generate explanation due to an error.', 'mismatch_explanation': 'N/A'}
        
#         results.append({
#             'candidate_id': candidate['candidate_id'],
#             'name': candidate['name'],
#             'position': candidate['position'],
#             'years_experience': candidate['years_experience'],
#             'work_experience': candidate['work_experience'],
#             'favorite_languages': candidate['favorite_languages'],
#             'technologies': candidate['technologies'],
#             'explanation': explanation
#         })

#     return jsonify({'status': 'success', 'matches': results}), 200

@simsearch_blueprint.route('/api/get_matching_candidates_with_explanation/<int:job_id>', methods=['GET'])
def get_matching_candidates_with_explanation_route(job_id):
    def generate():
        sim_search_service = SimilaritySearch()
        candidates = sim_search_service.find_matching_candidates(job_id)
        if candidates is None:
            yield json.dumps({'status': 'error', 'message': 'Job not found or embedding not generated'})
            return

        job = Job.query.get(job_id)
        job_text = f"{job.title} {job.description} {job.specialization} {' '.join(job.tech_stack)}"

        yield '{"status": "success", "matches": ['

        first = True
        for candidate in candidates:
            if not first:
                yield ','
            first = False

            candidate_text = f"{candidate['position']} {candidate['work_experience']} {' '.join(candidate['favorite_languages'])} {' '.join(candidate['technologies'])}"
            
            current_app.logger.info(f"Generating explanation for candidate {candidate['candidate_id']}")
            start_time = time.time()
            explanation = sim_search_service.generate_explanation(job_text, candidate_text)
            end_time = time.time()
            
            current_app.logger.info(f"Explanation generated in {end_time - start_time:.2f} seconds")
            
            if isinstance(explanation, dict) and 'error' in explanation:
                current_app.logger.error(f"Error generating explanation for candidate {candidate['candidate_id']}: {explanation['error']}")
                explanation = {'match_explanation': 'Unable to generate explanation due to an error.', 'mismatch_explanation': 'N/A'}
            
            result = {
                'candidate_id': candidate['candidate_id'],
                'name': candidate['name'],
                'position': candidate['position'],
                'years_experience': candidate['years_experience'],
                'work_experience': candidate['work_experience'],
                'favorite_languages': candidate['favorite_languages'],
                'technologies': candidate['technologies'],
                'explanation': explanation
            }
            
            yield json.dumps(result)

        yield ']}'

    return Response(stream_with_context(generate()), content_type='application/json')