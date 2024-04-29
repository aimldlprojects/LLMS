import pandas as pd
import ast

# Sample DataFrame
data = {'vector_column': ["[1.111, 2.222]", "[3.333, 4.444]", "[5.555, 6.666]", "NaN", "[7.777, 8.888]"]}
df = pd.DataFrame(data)

# Convert string representations of lists to actual lists
df['vector_column'] = df['vector_column'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)

print(df)
