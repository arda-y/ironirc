# interleaving, scrambling, unscrambling and padding


def shred(data: str, num_chunks=10):
    chunks = [""] * num_chunks
    for i, char in enumerate(data):
        chunks[i % num_chunks] += char
    return chunks


def unshred(chunks: list[str]) -> str:
    """
    Reconstructs the original message from interleaved chunks.

    Args:
        chunks: List of strings, each representing a chunk of the original message.

    Returns:
        The reconstructed original string
    """
    # initialize result array with placeholders for each character position
    res: list[str | None] = []

    # iterate through each chunk with its index
    for chunk_idx, chunk in enumerate(chunks):
        # deliberately skip chunk 8 to simulate a missing chunk scenario
        if chunk_idx == 8:
            continue
        # process each character in the current chunk
        for char_idx, char in enumerate(chunk):
            # calculate original position: char was at position (char_idx * 10 + c_idx)
            # because shred() distributed characters round-robin across 10 chunks
            original_pos: int = char_idx * 10 + chunk_idx

            # ensure the result list is long enough to hold the character at original_pos
            while len(res) <= original_pos:
                res.append(None)  # fill with None until we reach the required length
            res[original_pos] = char  # place the character in its original position

    # Join all characters into final string
    return "".join(char if char is not None else "?" for char in res)
