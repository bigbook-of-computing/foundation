# **Chapter 2: Precision, Error, and Numerical Judgment (Workbook)**

---

> **Summary:** This workbook explores the fundamental limits of digital representation. We move beyond treating numbers as exact values and begin to view them as finite-precision approximations. We will quantify **Machine Epsilon**, observe the growth of **absolute gaps** across magnitudes, and witness the catastrophic failure of **cancellation**. Mastering these concepts is the prerequisite for "Numerical Judgment"—the ability to predict when a calculation is safe and when it is on the verge of collapse.

---

## **2.1 Machine Epsilon & Representation** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** The Granularity of Zero
> 
> **Summary:** Computers do not have a continuum of numbers; they have a discrete grid. Machine Epsilon ($\epsilon_m$) defines the resolution of that grid near 1.0. This section teaches you how to measure this fundamental hardware constant.

---

### **Theoretical Background**

The IEEE 754 floating-point standard represents numbers as $sign \times mantissa \times 2^{exponent}$. Because the mantissa has a fixed number of bits (52 for `float64`), there is a smallest possible change we can make to a number.

**Machine Epsilon ($\epsilon_{m}$):** The smallest positive number such that $1.0 + \epsilon_{m} \neq 1.0$.
- For 64-bit doubles, $\epsilon_{m} \approx 2.22 \times 10^{-16}$.
- Any physical difference smaller than this is "invisible" to the computer at the scale of 1.0.

!!! tip "The Rule of 15"
    A simple rule of thumb: `float64` gives you approximately **15 to 17 decimal digits** of precision. If your physics requires 20 digits of accuracy, you cannot solve it with standard floating-point arithmetic.

---

### **Comprehension Check**

!!! note "Quiz"
    **1. Why does `0.1 + 0.2` not equal `0.3` exactly in binary?**
    
    - A. Binary numbers can only represent integers.
    - B. **The decimal value 0.1 is a repeating (non-terminating) sequence in binary that must be truncated.**
    - C. The CPU performs addition differently than human logic.
    - D. Standard Python uses 32-bit floats by default, which are too small.
    
    **2. If $x = 10^{16}$, what is the smallest number you can add to $x$ such that the computer notices the change?**
    
    - A. $1.0 \times 10^{-16}$
    - B. $1.0$
    - C. **Approximately 2.0, due to the absolute gap defined by Machine Epsilon.**
    - D. $10^{16}$ itself.

??? info "See Answer"
    **Correct: B, C**  
    1. **B.** Just as $1/3$ is $0.333...$ in decimal, the fraction $1/10$ is a repeating sequence in binary ($0.000110011...$). The computer must truncate this sequence, leading to a tiny representation error.
    2. **C.** At the scale of $10^{16}$, the absolute gap between representable numbers is $\epsilon_m \times 10^{16} \approx 2.22$. Any addition smaller than this will be "rounded away."

---

## **2.2 Catastrophic Cancellation** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** Loss of Significance
> 
> **Summary:** The most dangerous event in numerical physics is the subtraction of two nearly equal, large numbers. This "cancels" the shared leading digits, leaving only the random "noise" in the trailing bits.

---

### **Theoretical Background**

Consider $f(x) = \sqrt{x+1} - \sqrt{x}$ for very large $x$.
- Both terms are nearly identical.
- When subtracted, the significant digits cancel out.
- The result is dominated by round-off error.

!!! abstract "Interview-Style Question"
    
    You are modeling a satellite's orbit and need to calculate the difference between two distances that are both roughly $10^7$ meters but differ by only $10^{-3}$ meters. What numerical risk do you face, and how do you mitigate it?
    
    ???+ info "Answer Strategy"
        You face **Catastrophic Cancellation**. Since the numbers are large ($10^7$), the computer only tracks about 15 digits. The $10^{-3}$ difference sits at the 10th decimal place ($7 + 3 = 10$). While this is within the 15-digit limit, standard subtraction will discard the 7 matching leading digits, leaving you with only 5 digits of precision in your result.
        
        **Mitigation:**
        1. **Algebraic Reformulation:** Use identities like $(a-b) = (a^2-b^2)/(a+b)$ to avoid the subtraction.
        2. **Use Higher Precision:** Switch to `float128` if the hardware supports it (though this is a "brute force" fix).
        3. **Taylor Expansion:** For very small differences, use the first few terms of a Taylor series instead of the direct formula.

---

## **2.3 Hands-On Projects** {.heading-with-pill}

### **Project Blueprint: The Precision Audit**

| Component | Description |
| :--- | :--- |
| **Objective** | Quantify the loss of significance and the growth of representation gaps. |
| **Mathematical Concept** | Floating-point relative error and spacing logic. |
| **Experiment Setup** | Python, NumPy `finfo`, and `nextafter` functions. |
| **Process Steps** | 1. Calculate Epsilon. 2. Measure Gaps at $10^0$ to $10^{16}$. 3. Stress-test subtraction. |
| **Expected Behavior** | Absolute gaps should grow linearly with magnitude; relative gaps stay constant. |
| **Verification Goal** | Plot the "Staircase of Error" showing where precision collapses. |

---

#### **Outcome and Interpretation**

Executing this project proves that **Precision is not Absolute**. You will see that while you have 15 digits of precision relative to the number's size, the absolute "step size" between numbers grows massive for large values. This explains why we must always **scale** our physical problems (e.g., using atomic units instead of SI units) to keep our values near the $1.0$ range where the grid is finest.

---

## **Exit Ticket**

Before moving to **Chapter 3: Root Finding**, verify:
- [ ] I can explain why `1.0 + 1e-17 == 1.0` is True in Python.
- [ ] I can identify "Dangerous Subtractions" in a physics formula.
- [ ] I understand that "Conditioning" is a property of the *problem*, not the *algorithm*.