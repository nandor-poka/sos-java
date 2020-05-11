# sos-java

## Copyright (c) 2020, Dr. Nandor Poka

### Distributed under the terms of the 3-clause BSD License

Java Language module for the SoS jupyter kernel.

### Features

Direct data type conversion between Java and Python 3. Typesafety check for variables imported from other kernels.
Variable name and type is globally kept for variables coming from other kernels. If a variable with an existing name is passed, but the 
new type does not match the old type, the kernel automatically renames the incoming variable and warns the user.

### Conversion from Python to Java

|           **Python type(s)**                           | **Java type**     |
| :---                                               | ---:           |
| `None`      | `Void` with `null` value      |
| `bool`, `np.bool`     | `boolean` primitive      |
| `int`, `np.int8`, `np.int16`, `np.int32`, `np.int64` | `int` or `long` prmitive based on value |
| `float` | `float` primitive, support for `NaN` and +/- `infinity`  |
| `str`      |`String`      |
| `tuple`      | `HashSet` *     |
| `dict`      | `HashMap` *     |
| `list`      | array of corresponding primitive type (except `String`), eg.: `int[]` *     |

* Due to the limitation of the Java language `dict`, `tuple`, and `list` types are only converted if their elements are of the same type. Eg.a `list` of `["1", 2]` will not be converted.

### Conversion from Java to Python

|           **Java type(s)**                           | **Python type**     |
| :---                                               | ---:           |
| `boolean` | `bool`  |
| `Integer`, `Long`, `Float`, `Double`, `Short`, `Byte` or their primitive types| `int`|
| `float`   | `float` |
| `String`  | `str`   |
| `Map`     | `dict`  |
| `array`, eg. `int[]`| `list`    |
| `List`    | `list` |