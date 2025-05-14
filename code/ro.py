# Outside of synthesize(), define a method on your class:
def handle_incoming_chunk(self, chunk: bytes, stop_event):
    """
    Called whenever the network layer pushes down a new TTS audio chunk.
    Applies exactly the same buffering, timing, silence‐skipping,
    and first‐chunk callback logic as in on_audio_chunk.
    """
    # (Bring in all the same locals you'd use in the closure:)
    if stop_event.is_set():
        logger.info(
            f"👄🛑 {generation_string} Quick audio stream interrupted by stop_event. Text: {text[:50]}...")
        # We should not put more chunks, let the main loop handle stream stop
        return

    now = time.time()
    samples = len(chunk) // self._BPS
    play_duration = samples / self._SR

    # 2) Timing & logging
    if self._first_call:
        self._first_call = False
        self._prev_chunk_time = now
        ttfa = now - self._start_time
        logger.info(f"First audio in {ttfa:.2f}s")
    else:
        gap = now - self._prev_chunk_time
        self._prev_chunk_time = now
        if gap <= play_duration * 1.1:
            self._good_streak += 1
        else:
            self._good_streak = 0

    # 3) Buffering logic
    self._buffer.append(chunk)
    self._buffered_duration += play_duration
    if self._buffering:
        if self._good_streak >= 2 or self._buffered_duration >= 0.5:
            # flush buffer
            for c in self._buffer:
                self.audio_chunks.put_nowait(c)
            self._buffer.clear()
            self._buffered_duration = 0
            self._buffering = False
    else:
        self.audio_chunks.put_nowait(chunk)

    # 4) First‐chunk callback
    if not self._fired_first_callback:
        self._fired_first_callback = True
        if self.on_first_audio_chunk_synthesize:
            self.on_first_audio_chunk_synthesize()


async def stream_from_server(self, text, stop_event):
    # Prepare state
    self._first_call = True
    self._fired_first_callback = False
    self._buffering = True
    buffer = []
    good_streak = 0
    buffered_duration = 0.0
    start_time = time.time()
    self._prev_chunk_time = 0.0

    async for chunk in self.download_stream(url, params={"text": text}):
        if self.stop_event.is_set():
            break
        self.handle_incoming_chunk(chunk, stop_event)

    # After loop, do a final flush if needed
    if self._buffering and self._buffer:
        for c in self._buffer:
            self.audio_chunks.put_nowait(c)
        self._buffer.clear()

    async def download_stream(self, url, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                async for chunk in resp.content.iter_chunked(1024):
                    yield chunk
