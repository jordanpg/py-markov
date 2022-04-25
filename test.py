from pymarkov import markov

def test_link():
    """Test that links are properly added"""
    m = markov.Markov()
    assert len(m) == 0
    # Add one word, verify only one word is counted and the link was created
    m.add_link(m.start_flag, "test")
    assert len(m) == 1
    assert m.to_node(m.start_flag)["test"] == 1
    # Strengthen the word, verifiny still only word word exists but it is strengthened
    m.add_link(m.start_flag, "test")
    assert len(m) == 1
    assert m.to_node(m.start_flag)["test"] == 2
    # Add link to the end node, verify still one word, but it now links to the end node
    m.add_link("test", m.end_flag)
    assert m.to_node("test")[m.end_flag] == 1
    # Verify the AI generates the trained input
    assert m.generate() == ['test']

def test_sentence():
    """Test that sentences are properly processed"""
    m = markov.Markov()
    # Add one sentence and verify all words were added
    m.process_text("testing this thing")
    assert len(m) == 3
    # Assert that the only word which may start a sentence is "testing"
    assert m.to_node(m.start_flag).num_links == 1
    assert m.to_node(m.start_flag)["testing"] == 1
    # Verify current model output only produces the single trained sentence
    assert m.generate() == ['testing', 'this', 'thing']
    # Add another sentence, ensuring three more words are added
    m.process_text("testing this thing. add three more.")
    assert len(m) == 6
    # Assert that "thing" only connects to the end flag, showing the sentences are split
    assert m.to_node("thing").num_links == 1
    assert m.to_node("thing")[m.end_flag] == 2
    # Slightly modify to add one new word and link the two sentences together
    m.process_text("testing this thing add one more")
    assert len(m) == 7
    assert m.to_node("thing").num_links == 2
    assert m.to_node("thing")["add"] == 1

if __name__ == "__main__":
    test_link()
    test_sentence()
