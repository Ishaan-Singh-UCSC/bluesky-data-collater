from atproto import Client, client_utils


def main():
    client = Client()
    profile = client.login('ishnicucsc@gmail.com', 'ishaannicholasucsc')
    print('Welcome,', profile.display_name)

    # Below is how to post an item to your profile

    # post = client.app.bsky.feed.post.get
    # text = client_utils.TextBuilder().text('install league of legends @ ').link('league of legends', 'https://www.leagueoflegends.com/en-us/download/')
    # post = client.send_post(text)
    # client.like(post.uri, post.cid)


    # This reads all the items that you posted

    # posts = client.app.bsky.feed.post.list(client.me.did, limit=10)
    # for uri, post in posts.records.items():
    #     print(uri, post.text)

    # 

    data = client.get_timeline()

    feed = data.feed
    next_page = data.cursor
    # print(type(feed[1]), type(next_page))
    for item in feed:
        print(f"Author: {item.post.author.handle}")
        print(item.post.record.text)
        print("\n\n")
if __name__ == '__main__':
    main()