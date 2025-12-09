from collections import Counter

class ArithmeticCoder:
    def __init__(self, reference_msg: str, delimit=True):
        self.delimit = delimit
        self.delimiter = "#"
        self.eps = 1e-8

        reference_msg = self._delimit(reference_msg)
        counts = dict(Counter(reference_msg))
        self.encoder_table = {}
        self.decoder_symbols = []
        self.decoder_cum_probs = (
            []
        )  # store list of the cum probs so we don't have to call list(decoder_table.keys()) every time, which would make the efficiency of binary searching pointless.

        lower = 0
        for k in counts.keys():
            upper = lower + counts[k] / len(reference_msg)
            self.encoder_table[k] = (lower, upper)
            self.decoder_symbols.append(k)
            self.decoder_cum_probs.append((lower, upper))
            lower = upper

        print(self.decoder_symbols)

    def encode(self, msg: str) -> str:
        msg = self._delimit(msg)
        u_i = 0.0
        v_i = 1.0

        encoded_msg = ""

        for symbol in msg:
            lower, upper = self.encoder_table[symbol]
            curr_range = v_i - u_i

            v_i = u_i + upper * curr_range - self.eps
            u_i = u_i + lower * curr_range

            print(u_i, v_i, symbol)

        while True:
            if u_i >= 0.5:
                encoded_msg += "1"
                u_i -= 0.5
                v_i -= 0.5
            elif v_i < 0.5:
                encoded_msg += "0"
            else:
                if v_i == 0.5:
                    encoded_msg += "01"
                else:
                    encoded_msg += "1"
                break
            u_i *= 2
            v_i *= 2

        return encoded_msg

    def decode(self, msg: str) -> str:
        """Assumes well-formed msg with delimiter"""

        l = 0.0
        h = 1.0

        curr_v = self._bitstream_to_float(msg)

        decoded_msg = ""

        while True:
            curr_range = h - l
            symbol, (prob_low, prob_high) = self._decode_symbol(curr_v, l, curr_range)

            print(prob_low, prob_high, symbol)
            decoded_msg += symbol
            if symbol == self.delimiter:
                return decoded_msg

            h = prob_high
            l = prob_low

    def _delimit(self, msg: str) -> str:
        if not self.delimit:
            return msg
        if msg[-1] != self.delimiter:
            return msg + self.delimiter
        return msg

    def _bitstream_to_float(self, bitstream: str) -> float:
        ans = 0
        power = 1

        for c in bitstream:
            if c == "1":
                ans += 2 ** (-power)
            power += 1

        return ans

    def _decode_symbol(
        self,
        f: float,
        low: float,
        curr_range: float,
    ) -> tuple[str, tuple[float, float]]:
        l, r = 0, len(self.decoder_cum_probs)

        while l < r:
            m = (l + r) // 2
            middle = low + self.decoder_cum_probs[m][0] * curr_range

            if middle <= f:
                l = m + 1
            else:
                r = m
        l -= 1
        symbol = self.decoder_symbols[l]
        prob_low, prob_high = self.decoder_cum_probs[l]

        prob_high = low + prob_high * curr_range - self.eps
        prob_low = low + prob_low * curr_range

        return symbol, (prob_low, prob_high)


if __name__ == "__main__":
    reference_msg = input("Enter reference string to infer alphabet and probs: ")
    ac = ArithmeticCoder(reference_msg)

    msg_to_encode = input("Input msg to encode: ")
    encoded_msg = ac.encode(msg_to_encode)
    print("encoded_msg:", encoded_msg)
    decoded_msg = ac.decode(encoded_msg)

    print("original message:", msg_to_encode)
    print("encoded_msg:", encoded_msg)
    print("decoded_msg:", decoded_msg)
