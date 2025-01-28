# Newton-Raphson Method

The **Newton-Raphson method** is an iterative numerical technique used to find approximations of roots for a real-valued function $f(x)$. It is efficient and often converges rapidly when the initial guess is close to the actual root.

---

## The Newton-Raphson Formula

$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$

Where:
- $x_n$: The current approximation of the root.
- $x_{n+1}$: The next, improved approximation of the root.
- $f(x_n)$: The value of the function at $x_n$.
- $f'(x_n)$: The derivative of the function at $x_n$.

---

## Steps of the Newton-Raphson Method

1. **Choose an Initial Guess ($x_0$)**:
   - Start with an initial approximation $x_0$ for the root.
   - The closer the guess is to the actual root, the faster the method converges.

2. **Iterate Using the Formula**:
   - Compute $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$.
   - Repeat this process until the value converges to a root (the change between successive iterations is very small).

3. **Stop When Converged**:
   - The method stops when $|x_{n+1} - x_n| < \epsilon$, where $\epsilon$ is a small tolerance level.

---

## Example: Finding a Root of $f(x) = x^2 - 2$

We want to find the square root of 2 (root of $f(x) = x^2 - 2$).

### Step 1: Define the Function and Its Derivative
- $f(x) = x^2 - 2$
- $f'(x) = 2x$

### Step 2: Choose an Initial Guess
- Let $x_0 = 1.5$ (a reasonable guess for $\sqrt{2}$).

### Step 3: Apply the Iteration Formula
- $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$

#### Iteration 1 ($n = 0$):

$x_1 = 1.5 - \frac{(1.5)^2 - 2}{2(1.5)} = 1.5 - \frac{0.25}{3} = 1.4167$

#### Iteration 2 ($n = 1$):

$x_2 = 1.4167 - \frac{(1.4167)^2 - 2}{2(1.4167)} = 1.4142$

#### Iteration 3 ($n = 2$):

$x_3 = 1.4142 - \frac{(1.4142)^2 - 2}{2(1.4142)} = 1.4142$

The process converges to \( \sqrt{2} \approx 1.4142 \) in just a few steps.

---

## Advantages of the Newton-Raphson Method

1. **Fast Convergence**:
   - The method converges quadratically (errors are squared at each step) if the initial guess is close to the root.
   
2. **Simplicity**:
   - Easy to compute once the function and its derivative are known.

3. **Wide Applications**:
   - Useful for engineering, physics, and applied mathematics problems.

---

## Limitations of the Newton-Raphson Method

1. **Initial Guess Dependence**:
   - A poor choice of \( x_0 \) can lead to divergence or slow convergence.

2. **Derivative Issues**:
   - If \( f'(x_n) = 0 \) at any step, the method breaks down (division by zero).

3. **Non-Convergence**:
   - The method may not converge if the function is highly nonlinear, has inflection points near the root, or has multiple roots.


