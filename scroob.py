#Code by Toby, Owen, Diego, and GPT


from collections import Counter
from scrabble.location import Location, WIDTH, CENTER, HORIZONTAL, VERTICAL
from scrabble.move import PlayWord, ExchangeTiles


ALL_TILES = [True] * 7

# ---------------------------
# Trie implementation
# ---------------------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            ch = ch.lower()
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    def build_from_iterable(self, words):
        for w in words:
            if w and w.isalpha():
                self.insert(w.lower())


class Scroob:
    """
    Trie-based Scrabble AI with a leave-value heuristic.
    Compatible with GateKeeper interface used in the tournament harness.
    """
    def __init__(self, alpha=0.8, max_candidates_per_pattern=2000, dict_words=None, dict_path=None):
        """
        alpha: weight of leave-value added to immediate score (tuneable)
        max_candidates_per_pattern: cap to avoid pathological generation
        dict_words: optional iterable of words (e.g., DICTIONARY from board)
        dict_path: optional path to words.txt
        """
        self.gk = None
        self.alpha = alpha
        self.max_candidates_per_pattern = max_candidates_per_pattern
        self.trie = Trie()

        if dict_words is not None:
            self.trie.build_from_iterable(dict_words)
        else:
            # try to load words.txt near this file
            path = dict_path # or os.path.join(os.path.dirname(__file__), 'words.txt')
            loaded = False
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.trie.build_from_iterable(line.strip() for line in f)
                    loaded = True
            except Exception:
                loaded = False
            if not loaded:
                # fallback: try to import dictionary from board module (common in this project)
                try:
                    from scrabble import board as _board_mod
                    if hasattr(_board_mod, 'DICTIONARY'):
                        self.trie.build_from_iterable(_board_mod.DICTIONARY)
                        loaded = True
                except Exception:
                    try:
                        import board as _board_mod2
                        if hasattr(_board_mod2, 'DICTIONARY'):
                            self.trie.build_from_iterable(_board_mod2.DICTIONARY)
                            loaded = True
                    except Exception:
                        loaded = False
            # if still not loaded, trie will be empty -> AI will fallback to exchanging tiles

    def __str__(self):
        return "Scroob"

    def set_gatekeeper(self, gatekeeper):
        self.gk = gatekeeper

    # ---------------------------
    # Main chooser
    # ---------------------------
    def choose_move(self):
        if self.gk is None:
            raise RuntimeError("GateKeeper not set on AI")

        # If board empty, try first-move logic centered on CENTER
        if self._board_is_empty():
            m = self._play_first_move()
            if m:
                return m
            return ExchangeTiles(ALL_TILES)

        best_move = None
        best_value = float('-inf')
        hand = list(self.gk.get_hand())

        anchors = self._find_anchors()
        for anchor in anchors:
            for direction in (HORIZONTAL, VERTICAL):
                for left_ext in range(0, 8):  # up to 7 tiles to the left/up
                    start = anchor - self._mul_dir(direction, left_ext)
                    if not start.is_on_board():
                        continue
                    pattern = self._build_pattern_cells(start, direction)
                    max_len = len(pattern)
                    for L in range(2, max_len + 1):
                        segment = pattern[:L]
                        # require at least one existing tile overlap (connected play)
                        if not any(self._is_fixed_cell(x) for x in segment):
                            continue
                        candidates = self._generate_candidates_for_segment(segment, hand, cap=self.max_candidates_per_pattern)
                        for word in candidates:
                            try:
                                self.gk.verify_legality(word, start, direction)
                                sc = self.gk.score(word, start, direction)
                            except ValueError:
                                continue
                            remaining = self._remaining_after_play(word, hand)
                            leave = self._leave_value(remaining)
                            total_value = sc + self.alpha * leave
                            if total_value > best_value:
                                best_value = total_value
                                best_move = PlayWord(word, start, direction)
        if best_move:
            return best_move
        return ExchangeTiles(ALL_TILES)

    # ---------------------------
    # First move logic
    # ---------------------------
    def _play_first_move(self):
        hand = list(self.gk.get_hand())
        best_score = -1
        best_move = None
        for L in range(min(7, 15), 1, -1):  # word lengths
            for offset in range(0, L):
                start = Location(CENTER.r, CENTER.c) - self._mul_dir(HORIZONTAL, offset)
                if not start.is_on_board():
                    continue
                segment = ['.'] * L
                candidates = self._generate_candidates_for_segment(segment, hand, cap=self.max_candidates_per_pattern)
                for word in candidates:
                    try:
                        self.gk.verify_legality(word, start, HORIZONTAL)
                        sc = self.gk.score(word, start, HORIZONTAL)
                    except ValueError:
                        continue
                    remaining = self._remaining_after_play(word, hand)
                    leave = self._leave_value(remaining)
                    total_value = sc + self.alpha * leave
                    if total_value > best_score:
                        best_score = total_value
                        best_move = PlayWord(word, start, HORIZONTAL)
            if best_move:
                return best_move
        return None

    # ---------------------------
    # Candidate generation (trie DFS)
    # ---------------------------
    def _generate_candidates_for_segment(self, segment, hand, cap=1000):
        """
        segment: list of '.' or board letter (preserve letter case), starting at start.
                 For any board-letter position we *consume* that letter in the trie but append a SPACE ' '
                 into the returned candidate word (the Board expects spaces where tiles already exist).
        hand: list of tiles like ['a','t','_','e',...]
        returns list of candidate strings (lowercase letters for newly placed tiles,
        uppercase letter for tiles placed using blanks, and ' ' for positions that are already on the board).
        """
        results = []
        hand_count = Counter(hand)

        def dfs(node, pos, prefix, rack_count):
            if len(results) >= cap:
                return
            if pos == len(segment):
                if node.is_word:
                    results.append(prefix)
                return
            cell = segment[pos]
            if self._is_fixed_cell(cell):
                # Board already has a tile here: follow trie on that letter but append a space in the candidate
                letter_key = cell.lower()
                child = node.children.get(letter_key)
                if child:
                    dfs(child, pos + 1, prefix + ' ', rack_count)
                return
            else:
                # open cell: try all child letters that can be provided by rack (tile or blank)
                for child_letter, child_node in node.children.items():
                    if rack_count.get(child_letter, 0) > 0:
                        rack_count[child_letter] -= 1
                        dfs(child_node, pos + 1, prefix + child_letter, rack_count)
                        rack_count[child_letter] += 1
                    elif rack_count.get('_', 0) > 0:
                        # use a blank: append uppercase letter to indicate blank-used in that position
                        rack_count['_'] -= 1
                        dfs(child_node, pos + 1, prefix + child_letter.upper(), rack_count)
                        rack_count['_'] += 1

        dfs(self.trie.root, 0, '', hand_count.copy())
        return results

    # ---------------------------
    # Small helpers
    # ---------------------------
    def _is_fixed_cell(self, cell):
        return cell is not None and cell != '.'

    def _build_pattern_cells(self, start, direction):
        cells = []
        loc = Location(start.r, start.c)
        while loc.is_on_board():
            sq = self.gk.get_square(loc)
            if sq.isalpha():
                cells.append(sq)   # preserve case so we know letter key
            else:
                cells.append('.')
            loc += direction
        return cells

    def _board_is_empty(self):
        for r in range(WIDTH):
            for c in range(WIDTH):
                if self.gk.get_square(Location(r, c)).isalpha():
                    return False
        return True

    def _find_anchors(self):
        anchors = []
        if self._board_is_empty():
            return [CENTER]
        for r in range(WIDTH):
            for c in range(WIDTH):
                loc = Location(r, c)
                if self.gk.get_square(loc).isalpha():
                    continue
                for neighbor in (loc + HORIZONTAL, loc - HORIZONTAL, loc + VERTICAL, loc - VERTICAL):
                    if neighbor.is_on_board() and self.gk.get_square(neighbor).isalpha():
                        anchors.append(loc)
                        break
        return anchors

    def _mul_dir(self, direction, times):
        return Location(direction.r * times, direction.c * times)

    def _remaining_after_play(self, word, hand):
        """
        Return list of tiles remaining after playing `word`.
        Word uses:
          - ' ' for board tiles (those consumed from board, not rack)
          - lowercase letters for tiles played from rack
          - UPPERCASE letters for tiles played using blanks from rack
        """
        hand_count = Counter(hand)
        for ch in word:
            if ch == ' ':
                continue
            if ch.isupper():
                if hand_count.get('_', 0) > 0:
                    hand_count['_'] -= 1
                else:
                    # unexpected: try to decrement tile if present
                    lc = ch.lower()
                    if hand_count.get(lc, 0) > 0:
                        hand_count[lc] -= 1
            else:
                if hand_count.get(ch, 0) > 0:
                    hand_count[ch] -= 1
        remaining = []
        for k, v in hand_count.items():
            remaining.extend([k] * v)
        return remaining

    # ---------------------------
    # Leave-value heuristic
    # ---------------------------
    def _leave_value(self, remaining_tiles):
        if not remaining_tiles:
            return 0.0
        vowels = set('aeiou')
        rare_penalty = set('jqxz')
        common_bonus = set('tnrsld')
        score = 0.0
        vcount = 0
        ccount = 0
        for t in remaining_tiles:
            if t == '_':
                score += 1.0
            elif t in vowels:
                score += 0.7
                vcount += 1
            elif t in common_bonus:
                score += 0.4
                ccount += 1
            elif t in rare_penalty:
                score -= 0.6
                ccount += 1
            else:
                score += 0.05
                ccount += 1
        score -= 0.5 * abs(vcount - ccount)
        return score
