import java.io.*;
import java.sql.*;
import java.util.*;


public class CreateDB {

  // Get properties
  public static final String propsFile = "jdbc.properties";


  /**
   * Connect to DB
   * 
   * @return Connection object representing the connection
   * @throws IOException if properties file cannot be accessed
   * @throws SQLException if connection fails
   */

  public static Connection getConnection() throws IOException, SQLException
  {

    // Load properties
    FileInputStream in = new FileInputStream(propsFile);
    Properties props = new Properties();
    props.load(in);

    // Get drivers
    String drivers = props.getProperty("jdbc.drivers");
    if (drivers != null)
      System.setProperty("jdbc.drivers", drivers);

    // Obtain access parameters and use them to create connection
    String url = props.getProperty("jdbc.url");
    String user = props.getProperty("jdbc.user");
    String password = props.getProperty("jdbc.password");

    return DriverManager.getConnection(url, user, password);
  }


  /**
   * Creates a table to hold the data.
   *
   * @param database connection to database
   * @throws SQLException if table creation fails
   */

  public static void createTable(Connection database) throws SQLException
  {
    // Statement for creating DB
    Statement statement = database.createStatement();

    // Drop existing table, if present

    try {
      statement.executeUpdate("DROP TABLE students");
    }
    catch (SQLException error) {
      // Catch and ignore SQLException, as this merely indicates
      // that the table didn't exist in the first place!
    }

    // Create a fresh table

    statement.executeUpdate("CREATE TABLE sim_data ("
                          + "sensor_id CHAR(8) NOT NULL PRIMARY KEY,"
                          + "Tempurature INT NOT NULL,"
                          + "wind_speed INT NOT NULL,"
                          + "humidity INT NOT NULL,"
                          + "co2 INT NOT NULL)");

    statement.close();
  }


  /**
   * Adds data to the table.
   *
   * @param in source of data
   * @param database connection to database
   * @throws IOException if there is a problem reading from the file
   * @throws SQLException if insertion fails for any reason
   */

  public static void addData(Connection database)
   throws IOException, SQLException
  {
    // Prepare statement used to insert data

    PreparedStatement statement =
     database.prepareStatement("INSERT INTO sim_data VALUES(?,?,?,?,?)");

    statement.setInt(1, 1);
    statement.setInt(2, 12);
    statement.setInt(3, 20);
    statement.setInt(4, 45);
    statement.setInt(5, 750);

    statement.executeUpdate();

    statement.close();
  }


  /**
   * Main program.
   */

  public static void main(String[] argv)
  {
    Connection database = null;
 
    try {
      System.err.println("Attempting connection...");
      database = getConnection();
      System.out.println("Connection Successful. \nAttempting to create table");
      createTable(database);
      System.out.println("Database Created. \nAttempting to add data");
      addData(database);
    }
    catch (Exception error) {
      error.printStackTrace();
    }
    finally {

      // If database isn't empty make sure we close it
      if (database != null) {
        try {
          database.close();
        }
        catch (Exception error) {}
      }
    }
  }


}
