from schema import Schema

event_validator = Schema({'rss_feed': str, 'name': str})
participant_validator = Schema({'event_id': int})
approve_question_validator = Schema({'uestion_id': int, 'approved': bool})
