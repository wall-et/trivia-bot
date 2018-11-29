NUM_WRONG_GUESSES = 3
NUM_GOOD_GUESSES = 3
POINTS_PER_GOOD_GUESS = 2
POINTS_PER_WRONG_GUESS = -1

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
NUMBERS = set("1234567890")

HOST = None
DB = "WikiTrivi_DB"

PAGE_COL = "pages"
WORD_COL = "common_words"
USER_COL = "users"
FAILER_GIFS_COL = "fail_gifs"
WINNER_GIFS_COL = "win_gifs"

WIKI_EXLUDE_VALS = "list main"

NUMBERS_RESPONSES = ["No way I'm accepting that.",
                     "Are you kidding? you can't guess numbers or letters....",
                     "Nope! i don't accept numbers and letters",
                     "Didn't I tell you? no numbers or letters"]
COMMON_RESPONSES = ["C'mon,This word is way too common...",
                    "Nah, Be more original with your words.",
                    "I want some good content, Buddy. Too common",
                    "Your guesses are so boring. Too common",
                    "Don't just give me every day words."]
FAIL_RESPONSES = ["Nope! You're wrong. tries left: {}",
                  "Wrong! watch out! only {} wrong guesses left",
                  "That is a novice mistake... only {} more like that.",
                  "Don't just make up things. {} more mistakes for you.",
                  "Nah, Not a good guess this one. {} more",
                  "You sure you know it? only {} errors left."]
SUCCESS_RESPONSES = ["Way to go! you'll finish in {} guesses.",
                     "Alrighty! only {} words to guess.",
                     "You Rock! guess me {} more.",
                     "Your Knowledge is astounding. only {} more words",
                     "I worship your brain! c'mon {} and you're done."]
WIN_RESPONSES = ["You win!!!!!\nYour score is {}url{}", "and that's a win! with a score of {}url{}",
                 "BAM! win! with {} points.url{}",
                 "clap your hands for this one! win with a score of {}url{}",
                 "aaaaand you win! {} points! url{}"]
LOSE_RESPONSES = ["Nah, You failed this round.\n Your score is {}\nwould you like to hear about this subject?url{}",
                  "Hahaha fail! You're out with a score of {}.\nwanna learn about it?url{}",
                  "Sorry buddy you failed, maybe next round.\nyou got {} points.url{}",
                  # "GameOver.\nscore:{}url{}",
                  "So did you really know this one? I guess not, you failed! \n{} points for you. url{}"]
CHOOSE_VALUE = ["So have you heard about {}?",
                "really? what about {}?",
                "This too? so head of {}?",
                "Just pick one. {}?", ]
INVALID_ANSWERS = ["invalid answer.\nchoose 'yes' or 'no'."]
TITLE_REPONSES = ["hey, enter words about it...",
                  "You can't just reuse the title",
                  "I see what you did there...",
                  "No way I'm accepting that."]
REPEATING_GUESS = ["Nice try. can't fool me. you used this word already","No recycling words here."]
