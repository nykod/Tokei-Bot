from other.bot import DiscordClient


if __name__ == '__main__':
    client = DiscordClient.client
    DiscordClient().botEvents()
    client.run('') #insert token here
