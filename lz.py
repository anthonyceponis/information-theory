class LempelZivCoder:
    def __init__(self, reference_msg: str, delimit=True, dictionary_size=3):
        self.delimit = delimit
        self.delimiter = "#"

        self.dictionary_size = dictionary_size
        self.encode_dictionary = dict()
        self.decode_dictionary = dict()
        reference_msg = self._delimit(reference_msg)

        for char in reference_msg:
            if char not in self.encode_dictionary:
                code = self._to_unsigned_binary(
                    len(self.encode_dictionary), dictionary_size
                )
                self.encode_dictionary[char] = code
                self.decode_dictionary[code] = char

    def encode(self, msg: str) -> str:
        assert len(msg) > 0, "message must not be empty."
        msg = self._delimit(msg)

        encoded_msg = ""
        s = msg[0]

        encode_dictionary = self.encode_dictionary.copy()

        i = 0
        while i < len(msg):
            encoded_msg += encode_dictionary[s]
            i += len(s)

            if len(encode_dictionary) < 2**self.dictionary_size and i < len(msg):
                x = msg[i]
                encode_dictionary[s + x] = self._to_unsigned_binary(
                    len(encode_dictionary), self.dictionary_size
                )

            s = self.match_longest_dict_entry(msg[i:], encode_dictionary)

        return encoded_msg

    def decode(self, msg: str) -> str:
        """Assumes well-formed msg with delimiter"""
        assert (
            len(msg) % self.dictionary_size == 0
        ), "encoded msg must be divisible by dictionary size"

        decode_dictionary = self.decode_dictionary.copy()
        msg_chunked = [
            msg[i : i + self.dictionary_size]
            for i in range(0, len(msg), self.dictionary_size)
        ]

        decoded_msg = ""
        prev_s = ""

        for chunk in msg_chunked:
            if chunk in decode_dictionary:
                s = decode_dictionary[chunk]
            else:
                s = prev_s + prev_s[0]

            decoded_msg += s

            if prev_s and len(decode_dictionary) < 2**self.dictionary_size:
                code = self._to_unsigned_binary(
                    len(decode_dictionary), self.dictionary_size
                )
                decode_dictionary[code] = prev_s + s[0]

            prev_s = s

        return decoded_msg

    def _delimit(self, msg: str) -> str:
        if not self.delimit:
            return msg
        if msg[-1] != self.delimiter:
            return msg + self.delimiter
        return msg

    def match_longest_dict_entry(
        self, msg: str, encode_dictionary: dict[str, str]
    ) -> str:
        # NOTE: Could optimise using something like a trie but this is not the focus.
        longest_match = ""
        for pattern in encode_dictionary:
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
    print("encoded_msg:", encoded_msg)
    decoded_msg = lz.decode(encoded_msg)

    print("original message:", msg_to_encode)
    print("encoded_msg:", encoded_msg)
    print("decoded_msg:", decoded_msg)
