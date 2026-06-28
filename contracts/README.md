# YAML Contract Documentation

The YAML contract defines how a CSV file should be validated and cleaned.

## Supported types

Values from a CSV file are initially read as text.

The program temporarily converts them when necessary for validation.

| Type      | Description                               | Example                |
| --------- | ----------------------------------------- | ---------------------- |
| `str`     | Character string                          | `"Alice"`              |
| `int`     | Integer                                   | `"42"` → `42`          |
| `decimal` | Precise decimal number                    | `"1200.50"`            |
| `bool`    | True or false value                       | `"true"` → `True`      |
| `date`    | Valid calendar date in a supported format | `"14/06/2026"`         |
| `email`   | Valid email address                       | `"client@example.com"` |

The `email` type is a domain-specific type. The value remains a string, but its format is validated as an email address.

### Date type

The `date` type validates each value as a real calendar date.

The following input formats are supported:

```text
YYYY-MM-DD
DD/MM/YYYY
YYYY/MM/DD
DD-MM-YYYY
```

Examples of valid values:

```text
2026-06-14
14/06/2026
2026/06/14
14-06-2026
```

A date must also exist in the calendar:

```text
31/02/2026 → invalid
```

Using `type: date` validates the value but does not change its original representation.

To convert a valid date to the standard ISO `YYYY-MM-DD` format, use the `normalize_date` transformation.

After validation, values are written back as text in the cleaned CSV file.

---

## Column options

Column options are declared directly under each column name.

| Option     | Description                                | Example           |
| ---------- | ------------------------------------------ | ----------------- |
| `required` | Defines whether the column must be present | `required: true`  |
| `nullable` | Defines whether cells may be empty         | `nullable: false` |
| `unique`   | Defines whether values must be unique      | `unique: true`    |

The `required` option applies to the column itself.

If a column marked as required is missing, the CSV structure is considered invalid.

The `nullable` option applies to individual cells.

If `nullable` is set to `false`, an empty cell makes the row invalid.

The `unique` option applies to all values in the column.

If a value appears more than once, the later occurrence is considered invalid.

Example:

```yaml
email:
  type: email
  required: true
  nullable: false
  unique: true
```

---

## Validation rules

Validation rules are declared under the `rules` key.

| Rule             | Description                              | Example                                       |
| ---------------- | ---------------------------------------- | --------------------------------------------- |
| `min`            | Defines the minimum numeric value        | `min: 18` → `17` is invalid                   |
| `max`            | Defines the maximum numeric value        | `max: 120` → `121` is invalid                 |
| `min_length`     | Defines the minimum number of characters | `min_length: 3` → `"AB"` is invalid           |
| `max_length`     | Defines the maximum number of characters | `max_length: 10` → `"ABCDEFGHIJK"` is invalid |
| `allowed_values` | Restricts values to a predefined list    | `[pending, paid]` → `"unknown"` is invalid    |
| `regex`          | Requires the value to match a pattern    | `^[A-Z]{2}[0-9]{3}$` accepts `"BE123"`        |
| `starts_with`    | Requires a specific prefix               | `"INV-001"` starts with `"INV-"`              |
| `ends_with`      | Requires a specific suffix               | `"main.py"` ends with `".py"`                 |

Example:

```yaml
rules:
  min: 18
  max: 120
```

Example with allowed values:

```yaml
rules:
  allowed_values:
    - pending
    - paid
    - cancelled
```

When a value does not satisfy a validation rule, the row is considered invalid.

All detected errors are added to the CSV error report.

---

## Transformations

Transformations are declared under the `transformations` key and are applied in the listed order.

| Transformation    | Description                          | Example                              |
| ----------------- | ------------------------------------ | ------------------------------------ |
| `strip`           | Removes outer whitespace             | `"  Alice  "` → `"Alice"`            |
| `lower`           | Converts to lowercase                | `"ALICE"` → `"alice"`                |
| `upper`           | Converts to uppercase                | `"alice"` → `"ALICE"`                |
| `title`           | Capitalizes each word                | `"jean dupont"` → `"Jean Dupont"`    |
| `collapse_spaces` | Replaces repeated spaces             | `"Jean    Dupont"` → `"Jean Dupont"` |
| `remove_accents`  | Removes accents                      | `"Élodie"` → `"Elodie"`              |
| `format_decimal`  | Rounds and formats with two decimals | `"14.75416"` → `"14.75"`             |
| `normalize_date`  | Converts to ISO date format          | `"14/06/2026"` → `"2026-06-14"`      |

Example:

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

Cleaning transformations are applied before the transformed value is validated against its expected type and validation rules.

Some transformations, such as `format_decimal` and `normalize_date`, temporarily convert the value to the corresponding Python type before writing the normalized result back as text.
