def is_valid_strdigit(c, base=2):
    if type(c) is not str: return False  # Reject non-string digits
    if (type(base) is not int) or (base < 2) or (base > 36): return False  # Reject non-integer bases outside 2-36
    if base < 2 or base > 36: return False  # Reject bases outside 2-36
    if len(c) != 1: return False  # Reject anything that is not a single character
    if '0' <= c <= str(min(base - 1, 9)): return True  # Numerical digits for bases up to 10
    if base > 10 and 0 <= ord(c) - ord('a') < base - 10: return True  # Letter digits for bases > 10
    return False  # Reject everything else


def valid_strdigits(base=2):
    POSSIBLE_DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'
    return [c for c in POSSIBLE_DIGITS if is_valid_strdigit(c, base)]


def print_valid_strdigits(base=2):
    valid_list = valid_strdigits(base)
    if not valid_list:
        msg = '(none)'
    else:
        msg = ', '.join([c for c in valid_list])
    print('The valid base ' + str(base) + ' digits: ' + msg)


# Quick demo:
# Test 0: `eval_strfrac_test0` (1 point)

def check_eval_strfrac(s, v_true, base=2, tol=1e-7):
    v_you = eval_strfrac(s, base)
    assert type(v_you) is float, "Your function did not return a `float` as instructed."
    delta_v = v_you - v_true
    msg = "[{}]_{{{}}} ~= {}: You computed {}, which differs by {}.".format(s, base, v_true,
                                                                            v_you, delta_v)
    print(msg)
    assert abs(delta_v) <= tol, "Difference exceeds expected tolerance."



def is_valid_strfrac(s, base=2):
    return all([is_valid_strdigit(c, base) for c in s if c != '.']) \
           and (len([c for c in s if c == '.']) <= 1)


def eval_strfrac(s, base=2):
    assert is_valid_strfrac(s, base), "'{}' contains invalid digits for a base-{} number.".format(s, base)
    assert type(s) is str
    assert 2 <= base <= 36

    decimal = None
    number = s
    value = 0.0
    i = 0
    letters = list("abcdefghijklmnopqrstuvwxyz")
    if "." in s:
        s = s.split(".")
        number = s[0]
        decimal = s[1]
    else:
       number = s

    numrev = number[::-1]
    for num in numrev:
        try:
            num = int(num)
        except:
            num = int(letters.index(num)) + 10
        value += num * base ** i
        i += 1

    if decimal is not None:
        t = -1
        for num in decimal:
            try:
                num = int(num)
            except:
                num = int(letters.index(num)) + 10
            value += num * base ** t
            t -= 1

    return value

print(eval_strfrac('1101', 2))

HEX_TO_BINARY_CONVERSION_TABLE = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101',
                                  '6': '0110',
                                  '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100',
                                  'd': '1101',
                                  'e': '1110', 'f': '1111'}

HEX_TO_BINARY_CONVERSION_TABLE = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101',
                                  '6': '0110',
                                  '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100',
                                  'd': '1101',
                                  'e': '1110', 'f': '1111'}


def hex_to_binary(hex_string):
    binary_string = " "
    for character in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[character]
    return binary_string


def fp_bin(v):
    assert type(v) is float
    vhex = v.hex()
    if vhex == '0x1.0000000000000p+0':
        vhex = '0x1.0000000000001p+0'
    s1 = vhex.split("x")
    if s1[0] == "-0":
        s_sign = "-"
    else:
        s_sign = "+"

    s2 = s1[1]
    s2 = s2.split("p")
    exp = s2[1]
    if exp == "0":
        v_exp = 0
    else:
        v_exp = int(exp)

    s3 = str(s2[0])
    sign = []
    s_temp = None
    if v != 0.0:
        for s in s3:
            if s != ".":
                if s == s3[0]:
                    sign.append(1)
                else:
                    sign.append(str(hex_to_binary(s)))

            else:
                sign.append(s)
        s_temp = ''.join(map(str, sign))
        s_space = s_temp.replace(" ", "")
        s_signif = s_space

    else:
        s_signif = v

    if s_temp is None:
        s_signif = "{0:.52f}".format(v)
    #else:
    #    s_space = s_temp.replace(" ", "")
    #    s_signif = s_space

    return (s_sign, s_signif, v_exp)


#print(fp_bin(1.0 + (2**(-53))))

def eval_fp(sign, significand, exponent, base=2):
    assert sign in ['+', '-'], "Sign bit must be '+' or '-', not '{}'.".format(sign)
    assert is_valid_strfrac(significand, base), "Invalid significand for base-{}: '{}'".format(base, significand)
    assert type(exponent) is int

    fnum2 = []
    expo = 0
    fnum0 = eval_strfrac(significand, base)
    range1 = range(exponent, 0)
    range2 = range(0, exponent)
    if exponent < 0:
        for val in range1:
            expo += 1
        fnum3 = str(fnum0 / base ** expo)
    else:
        for val in range2:
            expo += 1
        fnum3 = str(fnum0 * base ** expo)

    if sign == '-':
        fnum3 = -(float(fnum3))

    fnum = float(fnum3)

    return fnum




import math

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def add_fp_bin(u, v, signif_bits):
    u_sign, u_signif, u_exp = u
    v_sign, v_signif, v_exp = v

    # You may assume normalized inputs at the given precision, `signif_bits`.
    assert u_signif[:2] == '1.' and len(u_signif) == (signif_bits + 1)
    assert v_signif[:2] == '1.' and len(v_signif) == (signif_bits + 1)

    value1 = eval_fp(u[0], u[1], u[2], base=2) + eval_fp(v[0], v[1], v[2], base=2)
    # value2 = float(value1)
    value3 = fp_bin(value1)
    #value = round(float(value3[1]), (signif_bits+1))
    value = value3[1][0:signif_bits+1]
    #value = truncate(float(value3[1]), (signif_bits + 2))
    valz = (value3[0], value, value3[2])

    return valz


# Test: `add_fp_bin_test`

def check_add_fp_bin(u, v, signif_bits, w_true):
    w_you = add_fp_bin(u, v, signif_bits)
    msg = "{} + {} == {}: You produced {}.".format(u, v, w_true, w_you)
    print(msg)
    assert w_you == w_true, "Results do not match."

u = ('+', '1.010010', 0)
v = ('-', '1.000000', -2)
w_true = ('+', '1.000010', 0)
check_add_fp_bin(u, v, 7, w_true)

u = ('+', '1.00000', 0)
v = ('+', '1.00000', -5)
w_true = ('+', '1.00001', 0)
check_add_fp_bin(u, v, 6, w_true)

u = ('+', '1.00000', 0)
v = ('-', '1.00000', -5)
w_true = ('+', '1.11110', -1)
check_add_fp_bin(u, v, 6, w_true)

u = ('+', '1.00000', 0)
v = ('+', '1.00000', -6)
w_true = ('+', '1.00000', 0)
check_add_fp_bin(u, v, 6, w_true)

u = ('+', '1.00000', 0)
v = ('-', '1.00000', -6)
w_true = ('+', '1.11111', -1)
check_add_fp_bin(u, v, 6, w_true)

print("\n(Passed!)")