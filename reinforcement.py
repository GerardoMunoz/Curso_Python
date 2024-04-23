import array
import random

class Matrix:
    def __init__(self, m, n, data=None):
        self.m = m  # number of rows
        self.n = n  # number of columns
        if data is None:
            self.data = array.array('f', [0.0] * (n * m))
        else:
            if len(data) != n * m:
                raise ValueError("Incorrect data length")
            self.data = array.array('f', data)

    def __getitem__(self, index):
        if isinstance(index,tuple):
      
           i, j = index
           if isinstance(i,int) and isinstance(j,int):
                if 0 <= i < self.m and 0 <= j < self.n:
                    return self.data[i * self.n + j]
                else:
                    raise IndexError("Matrix indices out of range")
           if isinstance(i,int) and isinstance(j,slice):
             raise IndexError("One slice is not allow yet ")
           if isinstance(i,slice) and isinstance(j,int):
             raise IndexError("One slice is not allow yet ")
           if isinstance(i,slice) and isinstance(j,slice):
                 start_i, stop_i, step_i = i.indices(self.m)
                 start_j, stop_j, step_j = j.indices(self.n)
                 sliced_data = [self.data[r * self.n + c] for r in range(start_i, stop_i, step_i) for c in range(start_j, stop_j, step_j)]
                 return Matrix(stop_i - start_i, stop_j - start_j, sliced_data)
           else:
                 raise IndexError("i,j indices are required")
        else:
            raise ValueError("i,j indices are required")

    def __setitem__(self, index, value):
        i, j = index
        if 0 <= i < self.m and 0 <= j < self.n:
            self.data[i * self.n + j] = value
        else:
            raise IndexError("Matrix indices out of range")

    def __add__(self, other):
        #print('add',self.m,self.n,other.m,other.n)
        if isinstance(other, Matrix) and self.n == other.n and self.m == other.m:
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] + other[i, j]
            return result
        else:
            raise ValueError("Matrices of different dimensions cannot be added")

    def __sub__(self, other):
        #print('sub',self.m,self.n,other.m,other.n)
        if isinstance(other, Matrix) and self.n == other.n and self.m == other.m:
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] - other[i, j]
            return result
        else:
            raise ValueError("Matrices of different dimensions cannot be subtracted")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] * other
            return result
        elif isinstance(other, Matrix):
            #print('mul',self.m,self.n,other.m,other.n)
            if self.n != other.m:
                raise ValueError("Number of columns of first matrix must be equal to number of rows of second matrix")
            result = Matrix(self.m, other.n)
            for i in range(self.m):
                for j in range(other.n):
                    for k in range(self.n):
                        result[i, j] += self[i, k] * other[k, j]
            return result
        else:
            raise ValueError("Multiplication not defined for these data types")

    def T(self):
        transposed_data = array.array('f', [0.0] * (self.n * self.m))
        for i in range(self.m):
            for j in range(self.n):
                transposed_data[j * self.m + i] = self.data[i * self.n + j]
        return Matrix(self.n, self.m, transposed_data)
    
    def __or__(self,other):
        """
        concatenate vertically
        """
        if isinstance(other, Matrix) and self.n == other.n :
            return Matrix(self.m + other.m, self.n,self.data+other.data)
        else:
            raise ValueError("Matrices of different dimensions cannot be added")

    def __and__(self, other):
        """
        Concatenate two matrices horizontally.

        Args:
            other (Matrix): The second matrix to concatenate.

        Returns:
            Matrix: The resulting matrix after horizontal concatenation.
        """
        if self.m != other.m:
            raise ValueError("Matrices must have the same number of rows to concatenate horizontally")
        
        concatenated_data = []
        for i in range(self.m):
            concatenated_data.extend(self.data[i*self.n : (i+1)*self.n])
            concatenated_data.extend(other.data[i*other.n : (i+1)*other.n])

        return Matrix(self.m, self.n + other.n, concatenated_data)



    def __str__(self):
        output = ""
        for i in range(self.m):
            row_str = " ".join(str(self[i, j]) for j in range(self.n))
            output += row_str + "\n"
        return output

class Perceptron:
    def __init__(self, input_size, output_size):
      # each row is an input or an output
        self.weights = Matrix(input_size, output_size,  [random.random() for _ in range(input_size * output_size)])  # Initialize weights randomly
        self.bias = Matrix( 1,output_size, [random.random() for _ in range(output_size)])  # Initialize biases randomly

    def predict(self, inputs):
        # Weighted sum of inputs with weights plus biases
        result = inputs * self.weights  + self.bias
        # Apply activation function (in this case, step function)
        return result#Matrix(result.m, result.n, [[1 if val > 0 else 0 for val in row] for row in result.data])

    def train(self, inputs, labels, learning_rate=0.1, epochs=1):
        for epoch in range(epochs):
            # Make a prediction
            predictions = self.predict(inputs)
            # Calculate the error
            error = labels - predictions
            # Update weights and biases using error and learning rate
            self.weights += inputs.T() * error * learning_rate
            self.bias += error * learning_rate




class Reinforcement:
  def __init__(self,n_in, n_out, list_outs,f_error):
    """
    n_in, n_out : number of inputs and outputs
    list_outs : a Matrix of spected outputs. each row is one output
    f_error : input -> realnumber that represents the error of that input

    """
    self.n_in = n_in
    self.n_out = n_out
    self.list_outs = list_outs
    self.f_error = f_error
    self.control = Perceptron( n_in, n_out)
    self.model = Percepton(n_in + n_out, n_out)
    self.input_old =None
    self.output_old =None



  def predict(self, input_):

    output =self.control.predict(input_)
    
    self.train(self.input_old,self.output_old,input_,output)

    self.input_old=input_
    self.output_old=output
    return pred
     
  
  def train(self , input_old ,  output_old , input_ , output):
      model.train(input_old & output_old,input_)
      out_selected=None
      min_error=None
      for out_i in self.list_outs:
          in_predic = model.predict(input_ & out_i)
          error_pred = f_error(in_predic)
          if (error_predic < min_error) or (None == min_error):
              min_error = error_predic
              out_selected= out_i
      control.train(input_,out_selected)        
          
      




# Example usage
# Define training data (inputs) and their respective labels (labels)
inputs = Matrix(2,3, [0, 0, 1, 
                       1, 0, 0])
labels = Matrix(2, 2, [0, 1,
                       1, 0])


# Create a perceptron with 2 inputs and 2 outputs
perceptron = Perceptron(input_size=inputs.n, output_size=labels.n)

# Define training data (inputs) and their respective labels (labels)
inputs = Matrix(1, 3, [0, 0, 1,])
labels = Matrix(1, 2, [0, 1,])

# Train the perceptron
perceptron.train(inputs, labels)

# Make predictions
print("Predictions after training:")
for i in range(inputs.m):
    input_i=inputs[i:i+1,:]#[i*inputs.n:(i+1)*inputs.n]
    prediction = perceptron.predict(input_i)
    print(f"Inputs: {input_i} -> Prediction: {prediction}")


