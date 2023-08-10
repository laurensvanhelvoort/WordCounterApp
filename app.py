import streamlit as st

import string
import pandas as pd
import nltk
nltk.download('punkt')


def count_words(input_string):
    return sum([i.strip(string.punctuation).isalpha() for i in input_string.split()])


def count_chars(input_string):
    return len(input_string)


def extract_sentences(input_string):
    return nltk.tokenize.sent_tokenize(input_string)


def word_frequency(input_string):
    tokens = [token.lower() for token in input_string.split()]
    clean_tokens = [''.join(char for char in item if char not in string.punctuation)
                    for item in tokens]

    token_frequencies = nltk.FreqDist(clean_tokens)
    sorted_token_frequency = dict((sorted(token_frequencies.items(), key=lambda item: item[1], reverse=True)))
    token_frequency_list = [(token, frequency) for token, frequency in sorted_token_frequency.items()]

    df = pd.DataFrame(
        token_frequency_list,
        columns=["Word", "Frequency"]
    )
    return df


def calculate_averages(input_string, sentences):
    if input_string and sentences:
        words = input_string.split()
        avg_word_len = round(sum(len(word) for word in words) / len(words), 1)

        avg_sent_len = round(sum(len(word.split()) for word in sentences) / len(sentences))

        return avg_word_len, avg_sent_len
    else:
        return 0, 0


def reading_time_estimate(word_cnt):
    avg_wps = 200 / 60
    reading_time = round(word_cnt / avg_wps)

    if reading_time < 60:
        return f"{reading_time} seconds"
    else:
        minutes = reading_time // 60
        seconds_remaining = reading_time % 60
        if seconds_remaining > 0:
            return f"{minutes} min {seconds_remaining} seconds"
        else:
            return f"{minutes} minutes"


def main():
    st.title("Word counter")
    st.write('<style>textarea::placeholder { color: #808080; }</style>', unsafe_allow_html=True)
    user_input = st.text_area("Press Ctrl + Enter to analyze your text", placeholder="Enter your text here...",
                              key="text_input", height=250)

    word_count = count_words(user_input)
    char_count = count_chars(user_input)

    st.write("---")
    st.header("Basic")
    st.subheader(f":blue[{word_count}] words and :blue[{char_count}] characters")

    st.write("---")

    st.header("Advanced")
    sentences = extract_sentences(user_input)
    st.markdown(f"#### :blue[{len(sentences)}] sentences")

    st.markdown(f"#### Reading time: :blue[{reading_time_estimate(word_count)}]")

    st.markdown("#### Averages")
    average_word_length, average_sentence_length = calculate_averages(user_input, sentences)
    st.markdown(f"- Average amount of characters in a word:  :blue[{average_word_length}]")
    st.markdown(f"- Average amount of words in a sentence: :blue[{average_sentence_length}]")

    st.markdown("#### Keyword Frequency")
    with st.expander("Click to expand/collapse"):
        st.table(word_frequency(user_input))


if __name__ == "__main__":
    main()
