import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from gpt_index import GPTSimpleVectorIndex

index = []

app = App(
    token=os.environ.get("ASKTHEDOCS_SLACK_BOT_TOKEN")
)

# listen for a direct message
@app.message("")
def message_hello(message, say):
  print("Received a message: " + message["text"])
  response = index.query(message["text"])
  print("Bot says: ", response)
  say(str(response))

# Start the app
if __name__ == "__main__":
  index = GPTSimpleVectorIndex.load_from_disk('pd-sdk-index.json')
  SocketModeHandler(app, os.environ["ASKTHEDOCS_SLACK_APP_TOKEN"]).start()
