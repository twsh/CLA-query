#!/usr/bin/env python3

code_to_usage_type = {
    '1': 'Photocopying',
    '2': 'Scanning',
    '8': 'Digital'
}
# The possible usage types

code_to_licence_type = {
    '132': 'Further Education',
    '134': 'Business',
    '136': 'Higher Education',
    '137': 'Law',
    '140': 'Extended Multinational',
    '141': 'Pharmaceutical',
    '143': 'Schools',
    '154': 'Public Sector',
    '230': 'Extended Pharmaceutical Multinational',
    '232': 'Media Monitoring',
    '234': 'Multinational',
    '235': 'Pharmaceutical Multinational'
}
# The possible licence types

headers_to_messages = {
    'NegativeHeader': 'Negative',
    'NeutralHeader': 'Neutral',
    'PositiveHeader': 'Positive',
    'WarningHeader': 'Warning'
}
# Map responses to messages to write in the output file
