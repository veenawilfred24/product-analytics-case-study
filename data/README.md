# Data

This project uses only the provided e-commerce behavior dataset:

`data/sample/sample_data.csv`

The dataset contains event-level user behavior with:

- `event_time`
- `event_type`
- `product_id`
- `category_id`
- `category_code`
- `brand`
- `price`
- `user_id`
- `user_session`

Generated analysis tables are saved in `data/processed/`.

No synthetic behavioral data is created. The A/B test module simulates only random assignment to Variant A or Variant B; conversion outcomes come from observed purchase behavior in the dataset.

