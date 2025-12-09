class LempelZivCoder:
    def __init__(self, reference_msg: str, delimit=True, dictionary_size=3):
        self.delimit = delimit
        self.delimiter = "#"

        self.dictionary_size = dictionary_size
        self.dictionary = dict()
        reference_msg = self._delimit(reference_msg)

        for char in reference_msg:
            if char not in self.dictionary:
                self.dictionary[char] = self._to_unsigned_binary(
                    len(self.dictionary), dictionary_size
                )

    def encode(self, msg: str) -> str:
        assert len(msg) > 0, "message must not be empty."
        msg = self._delimit(msg)

        final_code = ""
        longest_match = msg[0]

        i = 0
        while i < len(msg):
            final_code += self.dictionary[longest_match]
            i += len(longest_match)

            if len(self.dictionary) < 2**self.dictionary_size and i < len(msg):
                self.dictionary[longest_match + msg[i]] = self._to_unsigned_binary(
                    len(self.dictionary), self.dictionary_size
                )

            next_longest_match = self.match_longest_dict_entry(msg[i:])
            # print(longest_match, msg[i], self.dictionary)
            longest_match = next_longest_match

        return final_code

    def decode(self, msg: str) -> str:
        """Assumes well-formed msg with delimiter"""
        raise NotImplementedError()

    def _delimit(self, msg: str) -> str:
        if not self.delimit:
            return msg
        if msg[-1] != self.delimiter:
            return msg + self.delimiter
        return msg

    def match_longest_dict_entry(self, msg: str) -> str:
        # NOTE: Could optimise using something like a trie but this is not the focus.
        longest_match = ""
        for pattern in self.dictionary:
            if len(pattern) > len(msg) or len(pattern) < len(longest_match):
                continue
            if msg[: len(pattern)] == pattern:
                longest_match = pattern
        return longest_match

    def _to_unsigned_binary(self, x: int, bits: int):
        return format(x & ((1 << bits) - 1), f"0{bits}b")


if __name__ == "__main__":
    reference_msg = input("Enter reference string to infer alphabet: ")
    lz = LempelZivCoder(reference_msg)

    msg_to_encode = input("Input msg to encode: ")
    encoded_msg = lz.encode(msg_to_encode)
    # print("encoded_msg:", encoded_msg)
    # decoded_msg = lz.decode(encoded_msg)

    print("original message:", msg_to_encode)
    print("encoded_msg:", encoded_msg)
    # print("decoded_msg:", decoded_msg)
