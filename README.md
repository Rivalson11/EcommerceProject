
# Product Inventory and Recommendation System

## Project Summary
This project is an e-commerce product inventory and recommendation system built using Django, Docker, RabbitMQ, Celery, and SQLite. The system manages products, tracks inventory, processes purchases, and provides personalized product recommendations to users.

---

## Local Setup with Docker

### Prerequisites
- Install Docker and Docker Compose.

### Steps
1. Clone the project repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd project-directory
   ```
3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
4. Access the project in your browser at `http://127.0.0.1:8000`.

### Notes
- Ensure that RabbitMQ and Celery are running, as they are critical for asynchronous task management.
- SQLite is used for local storage; ensure Docker volume mapping is set up for persistent data.

---

## Project Design

### Components

- **Docker**: Used to containerize the project, ensuring consistent environments across deployments. The project includes containers for Django, RabbitMQ, Celery, and a worker process.
  
- **RabbitMQ**: Acts as a message broker for Celery, allowing asynchronous task handling for background jobs, such as generating reports or recommendations.

- **Celery**: Used for task management, handling asynchronous processing to ensure a responsive user experience. Tasks like report generation run as background processes.

- **jQuery**: Facilitates asynchronous interactions within the UI, handling AJAX requests to the backend, such as polling for report statuses or downloading files.

---

## Recommendation System: Detailed Breakdown

The recommendation system analyzes each user’s purchase and pre-purchase activity to calculate a score for each category and uses this to generate product recommendations.

### Step 1: Retrieve and Analyze User Activity

The system begins by gathering all **purchases** and **pre-purchases** related to the user, aiming to understand the user’s preferences:

1. **Retrieve Purchases and Pre-Purchases**:
   - **Purchases** represent confirmed past transactions with full weight.
   - **Pre-Purchases** represent items added to the cart but not purchased, so they are given a partial weight (0.5) to influence recommendations without full priority.

2. **Calculate Category Totals**:
   - For each **purchase** or **pre-purchase** entry, the quantity of each product’s category is counted.
   - For each product in a user’s purchases, it sums the quantities for each associated category, creating a **weighted count** of the user’s interest in each category.
   - Pre-purchase quantities are multiplied by 0.5 to reflect partial interest.

#### Example of Grouping by Category for Weighted Counts

| Category        | Purchase Quantity | Pre-Purchase Quantity | Weighted Count Calculation            | Final Weighted Count |
|-----------------|-------------------|-----------------------|---------------------------------------|-----------------------|
| Electronics     | 3                 | 1                     | (3 * 1) + (1 * 0.5)                  | 3.5                   |
| Home Appliances | 2                 | 0                     | (2 * 1) + (0 * 0.5)                  | 2                     |
| Clothing        | 1                 | 2                     | (1 * 1) + (2 * 0.5)                  | 2                     |

### Step 2: Apply Weighted Scores to Products

After identifying the user’s preferred categories, we focus on products within these categories. Here’s how it works:

1. **Generate Weighted Scores for Products**:
   - For each product in the database, apply the weighted score for each category if the product belongs to that category.
   - If a product is in multiple categories with weights, those scores are summed.

2. **Annotate Products by Weighted Score**:
   - Using the calculated scores, each product receives a **weighted score** that reflects user interest based on past activity in those categories.

### Step 3: Filter and Order Recommendations

With each product annotated by a weighted score, the system refines the list of recommendations:

1. **Filter Products**:
   - Products with a weighted score greater than zero are prioritized, ensuring they are relevant to the user’s interests.
   - Exclude products with zero stock to prevent out-of-stock recommendations.

2. **Order by Weighted and Popularity Scores**:
   - Products are first ordered by the **weighted score** (user preference) and then by **popularity score** (general popularity).
   - The top 4 products from this ordered list are selected as recommendations.

#### Example Table: Final Product Scoring and Ranking

| Product       | Category        | Category Weighted Score | Product Popularity | Product Weighted Score | Final Rank |
|---------------|-----------------|-------------------------|---------------------|------------------------|------------|
| Smartphone    | Electronics     | 3.5                     | 85                 | 3.5                    | 1          |
| Blender       | Home Appliances | 2                       | 50                 | 2                      | 2          |
| T-shirt       | Clothing        | 2                       | 70                 | 2                      | 3          |
| Headphones    | Electronics     | 3.5                     | 60                 | 3.5                    | 4          |

### Summary

This recommendation system achieves personalized recommendations by:
1. **Aggregating Purchase Data by Category**: Totals purchases and pre-purchases with weighted values per category.
2. **Assigning Scores to Products Based on Categories**: Scores each product by summing the category weights it belongs to.
3. **Filtering and Ordering by Interest and Popularity**: Filters in-stock products with positive scores, then orders them for optimal user relevance.

By grouping products by category and applying weighted counts, the system tailors recommendations according to the user’s demonstrated interest across categories and individual products. This approach balances personal preference with broader popularity to ensure that recommendations are relevant and popular.

---

## Final Notes
By following this documentation, developers can set up, understand, and extend the project as needed. The modular design with Docker, RabbitMQ, Celery, and jQuery provides a scalable framework for future enhancements.
