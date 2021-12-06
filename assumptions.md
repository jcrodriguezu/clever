1. The episode_1.txt file is a mocked result of and API call that allow the users fetch a podcast by the id
2. The data coming from the api contains all the the transcriptions in the episode in the same format as in episode_1.txt
3. The episode transcription can be stored in any storage (example s3), for that reason I think this is an api call
4. We only can get a transcription segment at a time, that means giving a start time and end time range that
have multiple transcriptions, we only can get one.