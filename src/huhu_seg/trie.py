#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TrieAC :

    def __init__(self) :
        self.tree = dict()
        self.tree['state'] = 0
        self.index = 0
        self.output = dict()
        self.failure = dict()
        self.goto = dict()

    def add(self, word) :
        tree = self.tree
        for char in word :
            if char in tree :
                tree = tree[char]
            else :
                tree[char] = dict()
                prev_state = tree['state']
                self.index += 1
                try :
                    self.goto[prev_state][char] = self.index
                except :
                    self.goto[prev_state] = dict()
                    self.goto[prev_state][char] = self.index
                tree = tree[char]
                tree['state'] = self.index
                tree['prev_state'] = prev_state

        self.goto[self.index] = dict()
        self.output[self.index] = word
        tree['end'] = True

    def gen_failure(self) :
        tree = self.tree
        self.failure[0] = 0
        for key in tree :
            if key == 'state' :
                continue
            self.failure[tree[key]['state']] = tree['state']

        for key in tree :
            if key == 'state' :
                continue
            queue = list()
            queue.append(tree[key])
            while len(queue) != 0 :
                next = queue.pop(0)
                # print(next)
                fail = self.failure.get(next['state'])
                if fail is None :
                    prev_state = next['prev_state']
                    for char in self.goto[prev_state] :
                        if self.goto[prev_state][char] == next['state'] :
                            cur_char = char
                            break
                    while True :
                        prev_state = self.failure[prev_state]
                        if self.goto[prev_state].get(cur_char, False) is not False :
                            self.failure[next['state']] = self.goto[prev_state][cur_char]
                            break
                        elif prev_state == 0 :
                            self.failure[next['state']] = 0
                            break
                for key in next :
                    if key == 'state' or key == 'prev_state' or key == 'end':
                        continue
                    queue.append(next[key])

    def search(self, word) :
        output_list = list()
        index = 0
        cur_state = 0
        for char in word :
            next_state = self.goto[cur_state].get(char)
            output = self.output.get(next_state)
            # print(next_state, output, char)
            if next_state is not None :
                cur_state = next_state
                if index + 1 < len(word) and self.goto[cur_state].get(word[index + 1]) is not None :
                    index += 1
                    continue
                elif output is not None :
                    output_list.append((output, index - len(output) + 1,
                        index))
                    cur_state = 0
            else :
                cur_state = self.failure[cur_state]
                next_state = self.goto[cur_state].get(char)
                if next_state is not None :
                    cur_state = next_state
                # else :
                    # cur_state = self.failure[cur_state]
            index += 1
        return output_list

