import pandas as pd
import praw
from prawcore.exceptions import Forbidden

# praw and reddit api
username = 'kacperekk6dev'
password = 'Nightcore67276!!'
user_agent = 'MaterialRecording160'
client_secret = 'Y7jjhPVqMVsJICK3MqcBfoZsFIiJzQ'
client_id = 'zvD9wlU3W8G74Fd_vq5YKA'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     username=username)


class RedditTopUsersInfo:

    def __init__(self, subreddit_name, no_subreddit_posts=100, no_user_posts=10):
        self.subreddit_name = subreddit_name
        self.no_user_posts = no_user_posts
        self.no_subreddit_posts = no_subreddit_posts

    def get_top_posts_info(self, type='top'):
        """
        :param type:
        :return: pandas dataframe, returns post_info_dataframe with info based on top subreddit posts
        post_info_dataframe has 4 cols:
        1: 'id' - id of a post (str)
        2: 'author' - username (str)
        3: 'score' - no of up_votes (int)
        4: 'subreddit' - name of a subreddit that the submission was posted on (str)
         """
        subreddit = reddit.subreddit(self.subreddit_name)
        post_info = []
        for subm in subreddit.top(limit=self.no_subreddit_posts):
            subred_info = []
            subred_info.append(subm.id)
            subred_info.append(str(subm.author))
            subred_info.append(int(subm.score))
            subred_info.append(subm.subreddit)
            post_info.append(subred_info)
        post_info_sorted = sorted(post_info, key=lambda x: x[1], reverse=True)
        print(pd.DataFrame(post_info_sorted, columns=['id', 'author', 'score', 'subreddit']))
        return pd.DataFrame(post_info_sorted, columns=['id', 'author', 'score', 'subreddit'])

    def get_top_users_info(self, info=True):
        self.top_posts_info_df = self.get_top_posts_info()
        self.freq_authors = self.top_posts_info_df[self.top_posts_info_df.author != 'None']
        self.freq_authors = self.freq_authors['author']

        if info:
            print(f"Length of freq_authors =  {len(self.freq_authors.unique())}")
            print(self.freq_authors.unique())

        return self.freq_authors.unique()

    def get_users_post(self, username, number=10):
        user = reddit.redditor(username)
        user_comments_info = []
        for comment in user.comments.new(limit=number):
            user_comments_info.append(str(comment.id))
            user_comments_info.append(str(username))
            user_comments_info.append(int(comment.score))
            user_comments_info.append(str(comment.subreddit.display_name))

        user_posts_df = pd.DataFrame([(user_comments_info[i], user_comments_info[i + 2], user_comments_info[i + 1],
                                       user_comments_info[i + 3]) for i in range(0, len(user_comments_info), 4)],
                                     columns=['id', 'score', 'user_name', 'subreddit_name'])
        return user_posts_df

    def scrap_celebrities(self):
        usernames_list = self.get_top_users_info()
        df = pd.DataFrame()
        df = df.fillna(0)
        for author in usernames_list:
            try:
                temp = self.get_users_post(author, self.no_user_posts)
                print(temp)
                df = pd.concat([df, temp])
            except Forbidden:
                print(f'{author} account deleted or banned')
        print(df.info())
        print(df)
        return df
