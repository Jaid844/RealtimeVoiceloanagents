import uuid
from loan_work.src.graph import WorkFlow


def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print(f"Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)


app = WorkFlow().app
thread_id = str(uuid.uuid4())
_printed = set()

config = {
    "configurable": {
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,

    }
}
#_printed = set()
#
#qn = [
#    "hellow",
#    "yeah a loan adjustment would be great",
#    "seems good to me",
#    "did you calculate it yet",
#    "Still the adjustment seem to be more steep"
#]
#
#
#def generator_object(question):
#    for message_chunk, metadata in app.stream(
#            {"messages": ("user", question), "name": "James"}, config, stream_mode="messages"
#    ):
#        if message_chunk.content:
#            yield message_chunk.content
