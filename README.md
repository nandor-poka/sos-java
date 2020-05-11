# sos-java

## Copyright (c) 2020, Dr. Nandor Poka

### Distributed under the terms of the 3-clause BSD License.

Java Language module for the SoS jupyter kernel.

### Features

Direct data type conversion between Java and Python 3.

### Conversion from Python to Java

|           **Python type(s)**                           | **Java type**     |
| :---                                               | ---:           |
| `None`      | `Void` with `null` value      |
| `bool`, `np.bool`     | boolean primitive      |
| `int`, `np.int8`, `np.int16`, `np.int32`, `np.int64` | `int` or `long` prmitive based on value |
| `float` | `float` primitive, support for `NaN` and +/- `infinity`  |
| `str`      |`String`      |
| `tuple`      | `HashSet` *     |
| `dict`      | `HashMap` *     |
| `list`      | array of corresponding primitive type (except `String`), eg.: `int[]` *     |

* Due to the limitation of the Java language `dict`, `tuple`, and `list` types are only converted if their elements are of the same type. Eg.a `list` of `["1", 2]` will not be converted. 