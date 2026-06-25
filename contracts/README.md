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

## Transformations

Transformations are declared under the `transformations` key.

| Transformation    | Description                 | Example                              |
| ----------------- | --------------------------- | ------------------------------------ |
| `strip`           | Removes outer whitespace    | `"  Alice  "` → `"Alice"`            |
| `lower`           | Converts to lowercase       | `"ALICE"` → `"alice"`                |
| `upper`           | Converts to uppercase       | `"alice"` → `"ALICE"`                |
| `title`           | Capitalizes each word       | `"jean dupont"` → `"Jean Dupont"`    |
| `collapse_spaces` | Replaces repeated spaces    | `"Jean    Dupont"` → `"Jean Dupont"` |
| `remove_accents`  | Removes accents             | `"Élodie"` → `"Elodie"`              |
| `format_decimal`  | Formats with two decimals   | `"14.75416"` → `"14.75"`             |
| `normalize_date`  | Converts to ISO date format | `"14/06/2026"` → `"2026-06-14"`      |

