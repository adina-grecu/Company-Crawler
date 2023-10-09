import json

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_total_websites(filename):
    with open(filename, 'r') as f:
        return len(f.readlines())

def calculate_coverage(data):
    # The coverage is simply the count of websites we have data for
    return len(data)

def calculate_fill_rates(data):
    phone_numbers_filled = 0
    social_media_links_filled = 0

    for entry in data:
        if entry['phone_numbers']:
            #check if at least one phone number is filled
            phone_numbers_filled += 1
        if entry['social_media_links']:
            #check if at least one social media link is filled
            social_media_links_filled += 1

    total_websites = len(data)

    # Calculate percentages
    phone_number_fill_rate = (phone_numbers_filled / total_websites) * 100
    social_media_fill_rate = (social_media_links_filled / total_websites) * 100

    return phone_number_fill_rate, social_media_fill_rate

def main():
    data = load_data('output.json')
    total_given_websites = get_total_websites('data/sample-websites.csv')
    
    coverage = calculate_coverage(data)
    phone_fill_rate, social_fill_rate = calculate_fill_rates(data)
    
    #write results in file
    with open('analysis_results.txt', 'w') as f:
        f.write(f"Total given websites: {total_given_websites}\n")
        f.write(f"Total websites crawled: {coverage} ({coverage / total_given_websites * 100:.2f}%)\n")
        f.write(f"Phone number fill rate: {phone_fill_rate:.2f}%\n")
        f.write(f"Social media links fill rate: {social_fill_rate:.2f}%\n")

if __name__ == "__main__":
    main()
