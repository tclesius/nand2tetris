from Const import R, S


class Converter:
    # this class does the main work of converting vm commands in assembly
    def __init__(self, file):
        self.file = file
        self.labelId = {}

    def _a_command(self, address):
        self.file.write(f"@{address}\n")

    def _c_command(self, dest, comp, jump=None):
        if jump:
            self.file.write(f"{comp};{jump}\n")
        else:
            self.file.write(f"{dest};{comp}\n")

    def _l_command(self, xxx):
        self.file.write(f"({xxx})\n")

    def _dec_sp(self):
        self._a_command(R.SP)
        self._c_command("M", "M-1")

    def _inc_sp(self):
        self._a_command(R.SP)
        self._c_command("M", "M+1")

    def gen_label(self, name):
        if not self.labelId.get(name):
            self.labelId[name] = 0  # init id
            return name + self.labelId[name]
        self.labelId[name] += 1
        return name + self.labelId[name]

    def jump(self, comp, jump):
        self._c_command(dest=None, comp=comp, jump=jump)

    def _pop_in_reg(self, segment, index):
        self.pop("D")  # D = pop()
        self._a_command(S.R(segment) + index)  # A = *(D + index)
        self._c_command("M", "D")  # *A = D

    def _pop_in_mem(self, segment, index):
        self._a_command(index)
        self._c_command("D", "A")
        self._a_command(S.R(segment))
        self._c_command("D", "D+M")
        self._a_command(R.TEMP)
        self._c_command("M", "D")
        self.pop("A")
        self._c_command("D", "M")
        self._a_command(R.TEMP)
        self._c_command("A", "M")
        self._c_command("M", "D")

    def pop(self, dest=None, segment=None, index=None):
        self._dec_sp()
        if segment and index:
            # pop in segment
            if segment in [S.LOCAL, S.ARGUMENT, S.THIS, S.THAT]: self._pop_in_mem(segment, index)
            if segment in [S.POINTER, S.TEMP]:  self._pop_in_reg(segment, index)
            if segment == [S.STATIC]: ...  # TODO
        else:
            # pop value to D or just get address
            self._a_command(R.SP)
            if dest == "D":
                self._c_command("D", "M")

    def _push_const(self, const):
        self._a_command(const)
        self._c_command("D", "A")
        self.push()

    def _push_from_reg(self, segment, index):
        self._a_command(S.R(segment) + index)
        self._c_command("D", "M")
        self.push()

    def _push_from_mem(self, segment, index):
        self._a_command(index)
        self._c_command("D", "A")
        self._a_command(S.R(segment))
        self._c_command("A", "D+M")
        self._c_command("D", "M")
        self.push()

    def push(self, segment=None, index=None):
        if segment and index:
            # push from segment
            if segment in [S.LOCAL, S.ARGUMENT, S.THIS, S.THAT]: self._push_from_mem(segment, index)
            if segment in [S.POINTER, S.TEMP]:  self._push_from_reg(segment, index)
            if segment == S.CONSTANT:  self._push_const(index)
            if segment == [S.STATIC]: ...  # TODO
        else:
            # push from D
            self._a_command(R.SP)
            self._c_command("A", "M")
            self._c_command("M", "D")
        self._inc_sp()

    def binary(self, operator):
        # +,-,|,& supported
        self.pop("D")
        self.pop("A")
        self._c_command("D", f"M{operator}D")
        self.push(R.SP)

    def unary(self, operator):
        self.pop("D")
        self.pop("A")
        self._c_command("D", f"{operator}M")
        if operator == "-":
            self._c_command("D", "D-1")
        if operator == "!":
            self._c_command("D", "D+1")
        self.push(R.SP)

    def compare(self, jump):
        self.pop("D")
        self.pop("A")
        self._c_command("D", "M-D")
        self._a_command(self.gen_label(jump))  # if true jump to label
        self.jump("D", jump)
        self._a_command(self.gen_label('N' + jump))
        self.jump('0', "JMP")
        self._l_command(self.labelId[jump])
        self._c_command("D", "-1")
        self._l_command(self.labelId['N' + jump])
        self.push(R.SP)

    def prev_frame_to_reg(self, dest):
        self._a_command(R.FRAME)
        self._c_command("AM", "M-1")
        self._c_command("D", "M")
        self._a_command(dest)
        self._c_command("M", "D")

