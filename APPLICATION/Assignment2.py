"""
CSC312 Database Practical Assignment 2
Team Name: Algorithm Admirals
Members: Avuyile Maxhwele (4123042), Martin Bafana Malaza (3708931),
         Ezile Mzilikazi (4323373), Tanday Mike Pike (4044896),
         Sophumelela Swartbooi (4151726)
File: garden_exchange_app.py

Purpose: Connect to the GardenExchange MySQL database and execute
         all required SQL queries (simple, medium, complex) to
         demonstrate the database's usefulness for the community
         garden produce exchange scenario.
"""

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate


# ----------------------------------------------------------------------
# Database configuration
# ----------------------------------------------------------------------
DB_CONFIG = {
    "host": "172.21.12.21",
    "port": 23373,
    "user": "4323373",
    "password": "!St4323373",  # Enter the password you use for Workbench
    "database": "GardenExchange"
}

# ----------------------------------------------------------------------
# Connection helper
# ----------------------------------------------------------------------
def get_connection():
    """Establish and return a MySQL connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✓ Connected to GardenExchange database")
            return connection
    except Error as e:
        print(f"✗ Connection failed: {e}")
        return None


# ----------------------------------------------------------------------
# Query execution helper
# ----------------------------------------------------------------------
def execute_query(connection, query, description):
    """Execute a single query and pretty-print the result."""
    print("\n" + "=" * 70)
    print(f"QUERY: {description}")
    print("=" * 70)

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if results:
            print(tabulate(results, headers=columns, tablefmt="grid"))
            print(f"\nTotal rows returned: {len(results)}")
        else:
            print("No results found.")

        cursor.close()
        return results

    except Error as e:
        print(f"✗ Query error: {e}")
        return None


# ----------------------------------------------------------------------
# Main application
# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("GARDEN EXCHANGE DATABASE APPLICATION")
    print("Community Garden Produce Exchange System")
    print("=" * 70)

    connection = get_connection()
    if not connection:
        return

    # ------------------------------------------------------------------
    # SIMPLE QUERIES (2)
    # ------------------------------------------------------------------
    simple_queries = [
        (
            """SELECT g.FirstName, g.LastName, g.Email,
                      COUNT(gp.PlotID) AS NumberOfPlots
               FROM GARDENER g
               LEFT JOIN GARDEN_PLOT gp ON g.GardenerID = gp.GardenerID
               GROUP BY g.GardenerID, g.FirstName, g.LastName, g.Email
               ORDER BY g.LastName, g.FirstName;""",
            "S1: List all gardeners and the number of plots they own"
        ),
        (
            """SELECT c.CropName, c.CropCategory
               FROM CROP c
               ORDER BY c.CropCategory, c.CropName;""",
            "S2: List all crops available in the exchange"
        )
    ]

    # ------------------------------------------------------------------
    # MEDIUM QUERIES (4)
    # ------------------------------------------------------------------
    medium_queries = [
        (
            """SELECT c.CropName,
                      COUNT(DISTINCT pc.PlotID) AS PlotsGrowing,
                      SUM(h.QuantityHarvested) AS TotalHarvested
               FROM CROP c
               JOIN PLOT_CROP pc ON c.CropID = pc.CropID
               LEFT JOIN HARVEST h ON pc.PlotCropID = h.PlotCropID
               GROUP BY c.CropID, c.CropName
               ORDER BY TotalHarvested DESC;""",
            "M1: Total harvest per crop type with plot count (JOIN + Aggregation)"
        ),
        (
            """SELECT g.FirstName, g.LastName,
                      SUM(pe.QuantityContributed) AS TotalContributed
               FROM GARDENER g
               JOIN GARDEN_PLOT gp ON g.GardenerID = gp.GardenerID
               JOIN PLOT_CROP pc ON gp.PlotID = pc.PlotID
               JOIN HARVEST h ON pc.PlotCropID = h.PlotCropID
               JOIN PRODUCE_EXCHANGE pe ON h.HarvestID = pe.HarvestID
               GROUP BY g.GardenerID, g.FirstName, g.LastName
               HAVING SUM(pe.QuantityContributed) > 10
               ORDER BY TotalContributed DESC;""",
            "M2: Gardeners who contributed more than 10 units (JOIN + HAVING)"
        ),
        (
            """SELECT m.FirstName, m.LastName,
                      COUNT(pr.RequestID) AS TotalRequests,
                      SUM(pr.QuantityRequested) AS TotalQuantityRequested
               FROM MEMBER m
               JOIN PRODUCE_REQUEST pr ON m.MemberID = pr.MemberID
               GROUP BY m.MemberID, m.FirstName, m.LastName
               ORDER BY TotalQuantityRequested DESC;""",
            "M3: Members with their request counts and total quantities (JOIN + Aggregation)"
        ),
        (
            """SELECT cd.CollectionDate, cd.Location,
                      COUNT(pr.RequestID) AS RequestsForDay,
                      SUM(pr.QuantityRequested) AS TotalQuantity
               FROM COLLECTION_DAY cd
               LEFT JOIN PRODUCE_REQUEST pr ON cd.CollectionDayID = pr.CollectionDayID
               GROUP BY cd.CollectionDayID, cd.CollectionDate, cd.Location
               ORDER BY cd.CollectionDate;""",
            "M4: Collection day summary with request counts (LEFT JOIN + Aggregation)"
        )
    ]

    # ------------------------------------------------------------------
    # COMPLEX QUERIES (4)
    # ------------------------------------------------------------------
    complex_queries = [
        (
            """SELECT g.FirstName AS GardenerFirstName,
                      g.LastName AS GardenerLastName,
                      c.CropName,
                      h.QuantityHarvested,
                      pe.QuantityContributed,
                      (h.QuantityHarvested - pe.QuantityContributed) AS Retained
               FROM GARDENER g
               JOIN GARDEN_PLOT gp ON g.GardenerID = gp.GardenerID
               JOIN PLOT_CROP pc ON gp.PlotID = pc.PlotID
               JOIN CROP c ON pc.CropID = c.CropID
               JOIN HARVEST h ON pc.PlotCropID = h.PlotCropID
               JOIN PRODUCE_EXCHANGE pe ON h.HarvestID = pe.HarvestID
               WHERE h.QuantityHarvested > 10
                 AND pe.QuantityContributed >= 8
               ORDER BY Retained DESC;""",
            "C1: Detailed harvest vs contribution per gardener (Multi-JOIN + Filters)"
        ),
        (
            """SELECT c.CropName,
                      (SELECT SUM(h2.QuantityHarvested)
                       FROM HARVEST h2
                       JOIN PLOT_CROP pc2 ON h2.PlotCropID = pc2.PlotCropID
                       WHERE pc2.CropID = c.CropID) AS TotalHarvested,
                      (SELECT SUM(pe2.QuantityContributed)
                       FROM PRODUCE_EXCHANGE pe2
                       JOIN HARVEST h3 ON pe2.HarvestID = h3.HarvestID
                       JOIN PLOT_CROP pc3 ON h3.PlotCropID = pc3.PlotCropID
                       WHERE pc3.CropID = c.CropID) AS TotalContributed
               FROM CROP c
               WHERE (SELECT SUM(h4.QuantityHarvested)
                      FROM HARVEST h4
                      JOIN PLOT_CROP pc4 ON h4.PlotCropID = pc4.PlotCropID
                      WHERE pc4.CropID = c.CropID) > 15
               ORDER BY TotalHarvested DESC;""",
            "C2: Crops with high harvest and their contribution totals (Correlated Subqueries)"
        ),
        (
            """SELECT m.FirstName, m.LastName,
                      COUNT(pr.RequestID) AS TotalRequests,
                      SUM(CASE WHEN pr.RequestStatus = 'Approved' THEN 1 ELSE 0 END) AS Approved,
                      SUM(CASE WHEN pr.RequestStatus = 'Pending' THEN 1 ELSE 0 END) AS Pending,
                      SUM(CASE WHEN pr.RequestStatus = 'Rejected' THEN 1 ELSE 0 END) AS Rejected,
                      SUM(CASE WHEN pr.RequestStatus = 'Collected' THEN 1 ELSE 0 END) AS Collected
               FROM MEMBER m
               LEFT JOIN PRODUCE_REQUEST pr ON m.MemberID = pr.MemberID
               GROUP BY m.MemberID, m.FirstName, m.LastName
               HAVING COUNT(pr.RequestID) > 0
               ORDER BY TotalRequests DESC;""",
            "C3: Member request status breakdown (CASE + Aggregation + HAVING)"
        ),
        (
            """SELECT c.CropCategory,
                      COUNT(DISTINCT c.CropID) AS CropsInCategory,
                      COUNT(DISTINCT pc.PlotID) AS PlotsUsed,
                      SUM(h.QuantityHarvested) AS TotalHarvested,
                      ROUND(AVG(h.QuantityHarvested), 2) AS AvgHarvestPerRecord
               FROM CROP c
               JOIN PLOT_CROP pc ON c.CropID = pc.CropID
               JOIN HARVEST h ON pc.PlotCropID = h.PlotCropID
               GROUP BY c.CropCategory
               HAVING SUM(h.QuantityHarvested) > 20
               ORDER BY TotalHarvested DESC;""",
            "C4: Crop category performance analysis (Multi-level Aggregation + HAVING)"
        )
    ]

    # ------------------------------------------------------------------
    # Execute all queries
    # ------------------------------------------------------------------
    print("\n\n" + "#" * 70)
    print("# SIMPLE QUERIES")
    print("#" * 70)
    for query, desc in simple_queries:
        execute_query(connection, query, desc)

    print("\n\n" + "#" * 70)
    print("# MEDIUM QUERIES")
    print("#" * 70)
    for query, desc in medium_queries:
        execute_query(connection, query, desc)

    print("\n\n" + "#" * 70)
    print("# COMPLEX QUERIES")
    print("#" * 70)
    for query, desc in complex_queries:
        execute_query(connection, query, desc)

    # ------------------------------------------------------------------
    # Clean up
    # ------------------------------------------------------------------
    connection.close()
    print("\n✓ All queries executed successfully. Connection closed.")


if __name__ == "__main__":
    main()