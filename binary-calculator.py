import tkinter as tk
from collections import deque

q = deque()
m = deque()
a = deque()
q1 = deque()
result = deque()
neg = False

def clear_deques():
    global q, m, a, q1, result
    q.clear()
    m.clear()
    a.clear()
    q1.clear()
    result.clear()

counter, step, button, flag = 1, 1, 1, 1

def show_board(task_description):
    if button == 1:
        current_text = text_output.get(1.0, tk.END)
        new_text = f"\t{'-'*45}\n"
        if task_description == "Initial":
            new_text += f"\t(M){(''.join(map(str, m))).ljust(7)}|\t (A){''.join(map(str, a)).ljust(7)}|\t (Q){''.join(map(str, q)).ljust(7)}|\t {task_description}\n\t{'-'*45}"
        else:
            new_text += f"\t{(''.join(map(str, m))).ljust(7)}|\t {''.join(map(str, a)).ljust(7)}|\t {''.join(map(str, q)).ljust(7)}|\t {task_description}\n\t{'-'*45}"
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, current_text + new_text)
    elif button == 2 or button == 3:
        current_text = text_output.get(1.0, tk.END)
        new_text = f"\t{'-'*45}\n"
        new_text += f"\tResult:{(''.join(map(str, a))).ljust(7)}\n"
        new_text += f"\t{'-'*45}\n"
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, current_text + new_text)
    else:
        current_text = text_output.get(1.0, tk.END)
        new_text = f"\t{'-'*45}\n"
        if task_description == "Initial":
            new_text += f"\t(M){(''.join(map(str, m))).ljust(7)}|\t (A){''.join(map(str, a)).ljust(7)}|\t (Q){''.join(map(str, q)).ljust(7)}|\t (Q[-1]){''.join(map(str, q1)).ljust(7)}|\t {task_description}\n\t{'-'*45}"
        else:
            new_text += f"\t{(''.join(map(str, m))).ljust(7)}|\t {''.join(map(str, a)).ljust(7)}|\t {''.join(map(str, q)).ljust(7)}|\t {''.join(map(str, q1)).ljust(7)}|\t {task_description}\n\t{'-'*45}"
            if flag == 0:
                new_text += f"\n\n\t\tresult:{''.join(map(str, result)).ljust(7)}\n"
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, current_text + new_text)

def shift_left():
    a.popleft()
    a.append(q[0])
    q.popleft()

def compute_twos_complement_m():
    global m
    for i in range(len(m)):
        m[i] = 1 if m[i] == 0 else 0
    carry = 1
    for i in range(len(m) - 1, -1, -1):
        total = m[i] + carry
        m[i] = total % 2
        carry = total // 2

def compute_twos_complement_result():
    global result, flag
    flag = 0
    for i in range(len(result)):
        result[i] = 1 if result[i] == 0 else 0
    carry = 1
    for i in range(len(result) - 1, -1, -1):
        total = result[i] + carry
        result[i] = total % 2
        carry = total // 2

def compute_twos_complement_q():
    global a
    for i in range(len(q)):
        q[i] = 1 if q[i] == 0 else 0
    carry = 1
    for i in range(len(q) - 1, -1, -1):
        total = q[i] + carry
        q[i] = total % 2
        carry = total // 2

def binary_addition():
    carry = 0
    for i in range(len(m) - 1, -1, -1):
        total = m[i] + a[i] + carry
        a[i] = total % 2
        carry = total // 2


def binary_subtraction():
    borrow = 0
    for i in range(len(m) - 1, -1, -1):
        diff = a[i] - m[i] - borrow
        if diff < 0:
            diff += 2
            borrow = 1
        else:
            borrow = 0
        a[i] = diff

def arithmetic_right_shift():
    q1.appendleft(q[-1])
    q1.pop()
    q.pop()
    q.appendleft(a[-1])
    a.pop()
    a.appendleft(a[0])

def division():
    global step
    text_output.insert(tk.END, f"\nStep {step}: ")

    if a[0] == 0:
        shift_left()
        show_board("Left shift")
        binary_subtraction()
        show_board("A=A-M")
    else:
        shift_left()
        show_board("Left shift")
        binary_addition()
        show_board("A=A+M")
        

    if a[0] == 1:
        q.append(0)
        show_board("A[msb]=1 so Q[0]=0")
    else:
        q.append(1)
        show_board("A[msb]=0 so Q[0]=1")

    global counter
    counter -= 1
    
    if counter == 0 and a[0] == 1:
        binary_addition()
        show_board("A = A + M")

    text_output.insert(tk.END, f"\n")
    step += 1

def multiplication():
    global step, result, flag, counter
    text_output.insert(tk.END, f"\nStep {step}: ")
    
    if q[-1] == q1[0]:
        arithmetic_right_shift()
        if counter == 1 and neg == True:
            result = a + q
            compute_twos_complement_result()
        show_board("Arithmetic Right shift")
    else:
        if q[-1] == 0 and q1[0] == 1:
            binary_addition()
            show_board("A = A + M")
        else:
            binary_subtraction()
            show_board("A = A - M")
        arithmetic_right_shift()
        if counter == 1 and neg == True:
            result = a + q
            compute_twos_complement_result()
        show_board("Arithmetic Right shift")
        
    counter -= 1

    text_output.insert(tk.END, f"\n")
    step += 1

window = tk.Tk()
window.title("Binary Calculator")

dividend_var = tk.StringVar()
divisor_var = tk.StringVar()

def perform_division():
    global counter, step
    global button
    button = 1
    try:
        text_output.delete(1.0, tk.END)
        clear_deques()
        step = 1

        x = dividend_var.get()
        if not x or any(digit not in {0, 1} for digit in map(int, str(x))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the dividend.")

        for i in range(len(x)):
            q.append(int(x[i]))

        counter = len(q)

        y = divisor_var.get()
        if not y or any(digit not in {0, 1} for digit in map(int, str(y))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the divisor.")

        for i in range(len(y)):
            m.append(int(y[i]))
            a.append(0)
        if len(x)>len(y):
            for i in range(len(x)-len(y)+1):
                m.appendleft(0)
                a.appendleft(0)
        else:
            m.appendleft(0)
            a.appendleft(0)

        text_output.insert(tk.END, "Initial: ")
        show_board("Initial")
        text_output.insert(tk.END, f"\n")
        while True:
            if counter != 0:
                division()
            else:
                break

    except ValueError as e:
        text_output.insert(tk.END, str(e))

def perform_multiplication():
    global counter, step, m, q
    global button, neg, flag
    flag = 1
    button = 0
    try:
        text_output.delete(1.0, tk.END)
        clear_deques()
        step = 1
        q1.appendleft(0)

        x = dividend_var.get()
        if not x or any(digit not in {0, 1} for digit in map(int, str(x))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the Operand.")

        for i in range(len(x)):
            m.append(int(x[i]))
            a.append(0)

        y = divisor_var.get()
        if not y or any(digit not in {0, 1} for digit in map(int, str(y))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the Multiplier.")

        for i in range(len(y)):
            q.append(int(y[i]))

        counter = len(y)

        if (m[0] == 1 and q[0] == 0) or (m[0] == 0 and q[0] == 1):
            neg = True
        else:
            neg = False
        
        if m[0] == 1:
            compute_twos_complement_m()
            if m[0] == 1:
                m.appendleft(0)
                a.appendleft(0)
        if q[0] == 1:
            compute_twos_complement_q()
            if q[0] == 1:
                q.appendleft(0)
                counter += 1

        text_output.insert(tk.END, "Initial: ")
        show_board("Initial")
        text_output.insert(tk.END, f"\n")
        while True:
            if counter != 0:
                multiplication()
            else:
                break

    except ValueError as e:
        text_output.insert(tk.END, str(e))


def perform_addition():
    global step, m, a
    global button
    button = 2
    try:
        text_output.delete(1.0, tk.END)
        clear_deques()

        x = dividend_var.get()
        if not x or any(digit not in {0, 1} for digit in map(int, str(x))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the Operands.")

        for i in range(len(x)):
            a.append(int(x[i]))

        y = divisor_var.get()
        if not y or any(digit not in {0, 1} for digit in map(int, str(y))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the Operands.")

        for i in range(len(y)):
            m.append(int(y[i]))
        
        if len(x)>len(y):
            for i in range(len(x)-len(y)):
                m.appendleft(0)
        elif len(y)>len(x):
            for i in range(len(y)-len(x)):
                a.appendleft(0)
        else:
            m.appendleft(0)
            a.appendleft(0)
            
        binary_addition()
        show_board("Number Added")

    except ValueError as e:
        text_output.insert(tk.END, str(e))

def perform_subtraction():
    global step, m, a
    global button
    button = 3
    try:
        text_output.delete(1.0, tk.END)
        clear_deques()

        x = dividend_var.get()
        if not x or any(digit not in {0, 1} for digit in map(int, str(x))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the Operands.")

        for i in range(len(x)):
            a.append(int(x[i]))

        y = divisor_var.get()
        if not y or any(digit not in {0, 1} for digit in map(int, str(y))):
            raise ValueError("Invalid input. Please enter a valid binary integer for the Operands.")

        for i in range(len(y)):
            m.append(int(y[i]))
        
        if len(x)>len(y):
            for i in range(len(x)-len(y)):
                m.appendleft(0)
        
        if len(y)>len(x):
            for i in range(len(y)-len(x)):
                a.appendleft(0)

        binary_subtraction()
        show_board("Number Subtracted")

    except ValueError as e:
        text_output.insert(tk.END, str(e))

# GUI elements
label_dividend = tk.Label(window, text="Enter Operand:")
entry_dividend = tk.Entry(window, textvariable=dividend_var)

label_divisor = tk.Label(window, text="Enter Divisor/Multiplier:")
entry_divisor = tk.Entry(window, textvariable=divisor_var)

button_divide = tk.Button(window, text="Divide", command=perform_division)
button_multiply = tk.Button(window, text="Multiply", command=perform_multiplication)
button_addition = tk.Button(window, text="Add", command=perform_addition)
button_subtraction = tk.Button(window, text="Subtract", command=perform_subtraction)

text_output = tk.Text(window, height=30, width=90)

# Layout
label_dividend.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
entry_dividend.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
label_divisor.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
entry_divisor.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
button_divide.grid(row=4, column=0, padx=5, pady=10)
button_multiply.grid(row=4, column=1, columnspan=2, pady=10)
button_addition.grid(row=6, column=0, padx=5, pady=10)
button_subtraction.grid(row=6, column=1, padx=5, pady=10)
text_output.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()