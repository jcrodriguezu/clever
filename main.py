from episode import PodcastEpisode, EpisodesAPI


def retrieve_segment_transcript(episode_id, start_time, end_time):
    eapi = EpisodesAPI()
    transcriptions = eapi.get_episode_transcriptions(episode_id)
    episode = PodcastEpisode(episode_id, transcriptions)
    return episode.transcriptions.get_transcription(start_time, end_time)


def test_case_1():
    retrieved = retrieve_segment_transcript("episode_1", 21, 24)
    actual = "Everybody really just about literally everybody was growing Red Delicious."
    assert retrieved == actual


def test_case_2():
    """
    Explanation of this test case.

    The following is the text from 8:00 to 8:04, i.e. from 480 to 484 seconds.
        when the honeycrisp finally get to the store, they do great

    This means that 11 words are spread across 4 seconds. Hence, we should return
    5.5 words corresponding to the 2 seconds of transcript requested. Since,
    half a word doesn't make sense, we will round up and return 6 words.
    """
    retrieved = retrieve_segment_transcript("episode_1", 480, 482)
    actual = "when the honeycrisp finally get to"
    assert retrieved == actual
    

def test_case_3():
    """"""
    retrieved = retrieve_segment_transcript("episode_1", 0, 0)
    actual = None
    assert retrieved == actual
    
    
def test_case_4():
    """"""
    retrieved = retrieve_segment_transcript("episode_1", 0, 1)
    actual = None
    assert retrieved == actual
    
    
def test_case_5():
    """"""
    try:
        retrieved = retrieve_segment_transcript("episode_1", 1, 0)
    except Exception as e:
        assert str(e) == "End time must be greater than start time"
        
        
def test_case_6():
    """Assumption: we only can get on transcription segment at a time.
    """
    retrieved = retrieve_segment_transcript("episode_1", 1, 36)
    actual = "When I was a kid, apples were garbage. They were called Red Delicious and they were red. They were not delicious. They looked beautiful, but then you bite into it, and almost always it would be mushy and mealy, just nasty."
    assert retrieved == actual


if __name__ == "__main__":
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
