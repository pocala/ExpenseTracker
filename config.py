from configparser import ConfigParser

def read_config(filename = 'app.ini', section ='mysql'): 
    #Create a ConfigParser object to handle INI file parsing
    config = ConfigParser()

    #Read the INI file
    config.read(filename)

    #Dictionary to store configuration data
    data = {}

    if config.has_section(section):
        # Retrieve all key-value pairs within the specified section using .items
        items = config.items(section)
        
        #Populate the data dictionary with key-value pairs
        for item in items:
            data[item[0]] = item[1]
    else:
        #Raise exception if the specified section is not found
        raise Exception(f'{section} Section not found in the {filename} file')
    # Return the populated data dictionary
    return data
if __name__ == '__main__':
    # Read the configuration from the default section ('mysql') in the app.ini file and store it as "config"
    config = read_config()
    # Display the obtained configuration
    print(config)
