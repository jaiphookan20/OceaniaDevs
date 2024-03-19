from db import PostgresDB
from flask import Flask, request, jsonify


class JobsService:

    def populate_job_feed(self, uid, pagination_key, offset):
        pass

    def bookmark_a_job(self, uid, job_id, timestamp):
        pass

    def marked_job_as_applied(self, uid, job_id, timestamp):
        pass
