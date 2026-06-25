# YAML Contract Documentation

The YAML contract defines how a CSV file should be validated and cleaned.

## General structure

Each column to be processed is declared under the `columns` key.

```yaml
columns:
  column_name:
    type:
    required:
    nullable:
    unique:
    rules: {}
    transformations: []
```

* `type` defines the expected value type;
* `required` indicates whether the column must be present;
* `nullable` indicates whether cells may be empty;
* `unique` indicates whether values must be unique;
* `rules` contains the validation rules;
* `transformations` contains the cleaning operations to apply.

## Complete example

```yaml
columns:
  email:
    type: email
    required: true
    nullable: false
    unique: true
    rules: {}
    transformations:
      - strip
      - lower

  age:
    type: int
    required: true
    nullable: false
    unique: false
    rules:
      min: 18
      max: 120
    transformations:
      - strip
```

In this example:

* the `email` column must be present;
* its values cannot be empty or duplicated;
* leading and trailing whitespace is removed;
* letters are converted to lowercase;
* the email address format is then validated;
* the age must be between `18` and `120`.

---

## Supported types

Values from a CSV file are initially read as text.

The program temporarily converts them when necessary for validation.

| Type      | Description                | Example                |
| --------- | -------------------------- | ---------------------- |
| `str`     | Character string           | `"Alice"`              |
| `int`     | Integer                    | `"42"` → `42`          |
| `decimal` | Precise decimal number     | `"1200.50"`            |
| `bool`    | True or false value        | `"true"` → `True`      |
| `date`    | Date in an accepted format | `"14/06/2026"`         |
| `email`   | Valid email address        | `"client@example.com"` |

The `email` type is a domain-specific type. The value remains a string, but its format is validated as an email address.

After validation, values are written back as text in the cleaned CSV file.

---

## Column options

### `required`

Indicates whether the column must be present in the CSV file.

```yaml
required: true
```

If the column is missing, the file structure is considered invalid.

### `nullable`

Indicates whether a cell may be empty or null.

```yaml
nullable: false
```

An empty cell then makes the row invalid.

### `unique`

Indicates whether every value in the column must be unique.

```yaml
unique: true
```

Example:

```text
INV-001
INV-002
INV-001  ← duplicate
```

The second occurrence of `INV-001` is invalid.

---

## Validation rules

Validation rules are declared under the `rules` key.

| Rule             | Description                       | Example                                       |
| ---------------- | --------------------------------- | --------------------------------------------- |
| `min`            | Minimum numeric value             | `min: 18` → `17` is invalid                   |
| `max`            | Maximum numeric value             | `max: 120` → `121` is invalid                 |
| `min_length`     | Minimum number of characters      | `min_length: 3` → `"AB"` is invalid           |
| `max_length`     | Maximum number of characters      | `max_length: 10` → `"ABCDEFGHIJK"` is invalid |
| `allowed_values` | List of accepted values           | `[pending, paid]` → `"unknown"` is invalid    |
| `regex`          | Pattern that the value must match | `^[A-Z]{2}[0-9]{3}$` accepts `"BE123"`        |
| `starts_with`    | Required prefix                   | `"INV-001"` starts with `"INV-"`              |
| `ends_with`      | Required suffix                   | `"main.py"` ends with `".py"`                 |

### Example

```yaml
rules:
  min: 18
  max: 120
```

### Example with allowed values

```yaml
rules:
  allowed_values:
    - pending
    - paid
    - cancelled
```

When a value does not satisfy a validation rule, the row is considered invalid.

All errors detected in the row are added to the error report.

---

## Transformations

Transformations are declared under the `transformations` key.

| Transformation    | Description                                     | Example                              |
| ----------------- | ----------------------------------------------- | ------------------------------------ |
| `strip`           | Removes leading and trailing whitespace         | `"  Alice  "` → `"Alice"`            |
| `lower`           | Converts letters to lowercase                   | `"ALICE"` → `"alice"`                |
| `upper`           | Converts letters to uppercase                   | `"alice"` → `"ALICE"`                |
| `title`           | Capitalizes the first letter of each word       | `"jean dupont"` → `"Jean Dupont"`    |
| `collapse_spaces` | Replaces consecutive spaces with a single space | `"Jean    Dupont"` → `"Jean Dupont"` |
| `remove_accents`  | Removes accents from characters                 | `"Élodie"` → `"Elodie"`              |

### Example

```yaml
transformations:
  - strip
  - lower
```

The following value:

```text
"  CLIENT@EXAMPLE.COM  "
```

becomes:

```text
"client@example.com"
```

The transformations clean the value. The `email` type then verifies that the resulting value matches the expected email address format.
