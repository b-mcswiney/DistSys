import java.io.*;
import java.sql.*;
import java.util.*;


/**
 * Example of how to change the database password using JDBC.
 *
 * Usage: java PasswordDB
 *
 * @author Karim Djemame
 * @version 1.0 [2022-10-20]
 */

public class PasswordDB {


  public static final String propsFile = "jdbc.properties";


  /**
   * Establishes a connection to the database.
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

    // Define JDBC driver

    String drivers = props.getProperty("jdbc.drivers");
    if (drivers != null)
      System.setProperty("jdbc.drivers", drivers);
      // Setting standard system property jdbc.drivers
      // is an alternative to loading the driver manually
      // by calling Class.forName()

    // Obtain access parameters and use them to create connection

    String url = props.getProperty("jdbc.url");
    String user = props.getProperty("jdbc.user");
    String password = props.getProperty("jdbc.password");

    return DriverManager.getConnection(url, user, password);
  }

  /**
   * Main program.
   */

  public static void main(String[] argv)
  {
  
    Connection connection = null;
    
    try {
	// Establish the connection to the DB	
      connection = getConnection();

      // Create a mySQL statement and execute
      // This is an example! The password is hard coded but should not be
      String sql = "SET PASSWORD = PASSWORD('bluepainting')";
      Statement stmt = connection.createStatement();
      stmt.executeQuery(sql);
      stmt.close();
      System.out.println("Password is changed successfully!");	      
    }
    catch (Exception error) {
      error.printStackTrace();
    }
    finally {

      // This will always execute, even if an exception has
      // been thrown elsewhere in the code - so this is
      // the ideal place to close the connection to the DB...

      if (connection != null) {
        try {
          connection.close();
        }
        catch (Exception error) {}
      }
    }
  }


}
