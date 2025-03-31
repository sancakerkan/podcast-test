import yaml
import xml.etree.ElementTree as xml_tree

# Open and read the YAML file
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    # Create the root RSS element with required namespaces
    rss_element = xml_tree.Element('rss', {'version': '2.0',
                                           'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd', 
                                           'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'})
    
    # Create the channel element
    channel_element = xml_tree.SubElement(rss_element, 'channel')

    # Define the link prefix
    link_prefix = yaml_data['link']

    # Add elements to the channel
    xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
    xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
    xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
    xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']  # Fixed typo here
    xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
    xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
    xml_tree.SubElement(channel_element, 'link').text = link_prefix
    xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

    # Loop through items and add them to the channel
    for item in yaml_data['item']:
        item_element = xml_tree.SubElement(channel_element, 'item')
        xml_tree.SubElement(item_element, 'title').text = item['title']
        xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
        xml_tree.SubElement(item_element, 'description').text = item['description']
        xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
        xml_tree.SubElement(item_element, 'pubDate').text = item['published']

        # Clean up the 'length' field to remove commas and convert to integer
        length = item['length'].replace(',', '')  # Remove commas
        xml_tree.SubElement(item_element, 'enclosure', {
            'url': link_prefix + item['file'],
            'type': 'audio/mpeg',
            'length': str(length)  # Ensure length is a string
        })

    # Function to pretty-print XML with indentation
    def indent_xml(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for e in elem:
                indent_xml(e, level + 1)
            if not e.tail or not e.tail.strip():
                e.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    indent_xml(rss_element)

    # Write the updated and indented XML tree to the file
    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
