from extensions import db
from models import Job, Recruiter, Company, Application, Bookmark, Candidate
import openai
from utils.openai import get_embedding
import numpy as np
from sqlalchemy import text
from openai import OpenAI

class SimilaritySearch:
    """
    A class that provides methods for similarity-based job and candidate matching.
    """
    @staticmethod
    def generate_job_embedding(job_id):
        """
        Generate and store an embedding for a specific job.
        Args:
            job_id (int): The ID of the job to generate an embedding for.
        Returns:
            list: The generated embedding, or None if the job is not found.
        """
        # Retrieve the job from the database
        job = Job.query.get(job_id)
        if not job:
            return None
        
        # Combine job details into a single text string
        job_text = f"{job.title} {job.description} {job.specialization} {' '.join(job.tech_stack)}"
        
        # Generate the embedding using the OpenAI API
        embedding = get_embedding(job_text)
        
        # Convert numpy array to list if necessary
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        
        # Ensure the embedding has the expected length (1536 for OpenAI's embeddings)
        if len(embedding) != 1536:
            raise ValueError(f"Expected embedding of length 1536, but got {len(embedding)}")
        
        # Store the embedding in the job record and commit to the database
        job.embedding = embedding
        db.session.commit()    
        
        return embedding

    @staticmethod
    def find_matching_candidates(job_id, limit=20):
        """
        Find candidates that match a specific job based on embedding similarity.

        Args:
            job_id (int): The ID of the job to find matches for.
            limit (int): The maximum number of matches to return.
        Returns:
            list: A list of dictionaries containing matching candidate information,
                  or None if the job is not found or has no embedding.
        """
        # Retrieve the job and its embedding
        job = Job.query.get(job_id)
        if not job or job.embedding is None:
            return None

        job_embedding = job.embedding.tolist() if isinstance(job.embedding, np.ndarray) else job.embedding

        # Execute a raw SQL query to find the most similar candidates
        # This uses PostgreSQL's vector similarity operator '<->'
        candidates = db.session.execute(
            text("""
                SELECT candidate_id, name, position, years_experience, work_experience, favorite_languages, technologies
                FROM candidates
                ORDER BY embedding <-> :job_embedding
                LIMIT :limit;
            """),
            {'job_embedding': job_embedding, 'limit': limit}
        ).fetchall()

        # Format the results as a list of dictionaries
        matches = [{"candidate_id": row.candidate_id, "name": row.name, "position": row.position, 
                    "years_experience": row.years_experience, "work_experience": row.work_experience, 
                    "favorite_languages": row.favorite_languages, "technologies": row.technologies} 
                   for row in candidates]
        return matches
    
    @staticmethod
    def generate_explanation(job_text, candidate_text):
        """
        Generate an explanation for why a candidate is a good match for a job using GPT-4.

        Args:
            job_text (str): A string containing job details.
            candidate_text (str): A string containing candidate details.
        Returns:
            str: An explanation of why the candidate matches the job.
        """
        # Initialize the OpenAI client
        client = OpenAI(api_key="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")

        # Prepare the messages for the GPT-4 model
        messages = [
            {"role": "system", "content": "You are a job matching assistant."},
            {"role": "user", "content": f"Job Description: {job_text}\n\nCandidate Resume: {candidate_text}\n\nExplain why this candidate is a good match for the job."}
        ]
        
        # Make an API call to OpenAI's GPT-4 model
        response = client.chat.completions.create(
            model="gpt-4",  # Changed from "gpt-4o" to "gpt-4"
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        
        # Extract and return the generated explanation
        explanation = response.choices[0].message.content.strip()
        return explanation