import pickle
from flask import Flask, request, render_template, Response
from markupsafe import escape

app = Flask(__name__)
processed_df = pickle.load(open('proceesed_data_frame.pkl', 'rb'))

type_of_customer_to_cluster_mapping = {'New Customer': 0, 'Lost Customer': 1, 'Best Customer': 2, 'At Risk Customer': 3}
type_of_customer_to_recommended_action_mapping = {'New Customer': 'Need to handle with care by improving relationships with them.Company \
                                          should try to enhance their purchasing experience by providing good quality products and services and customer services.',
                                                  'Lost Customer': 'These cutomers may have already exited from the customer '
                                                                   'base.The company should try to undesratand why they left '
                                                                   'the system so that it does not happen again.',
                                                  'Best Customer': 'Potential to be the target of the new products made by the company and can increase company revenue by repeated advertising.Heavy discounts are not required.',
                                                  'At Risk Customer': 'At risk of churning.Need to be addressed urgently with focused advertising. May perform well if discounts are provided to them. Company should find out why they are leaving.'}


def get_customer_insights(customer_id: int):
    """
    method for analysing the customer based on the customer_id and retrieve insights about what 
    type of customer the person is and what sort of actions the company should take to retain the 
    customer
    """
    type_of_customer: str = ''
    mask = processed_df['CustomerID'].values == customer_id
    df_new = processed_df.loc[mask]
    for key, val in type_of_customer_to_cluster_mapping.items():
        if df_new['Cluster'].values == val:
            type_of_customer = key
    for key, val in type_of_customer_to_recommended_action_mapping.items():
        if key == type_of_customer:
            return {'Type of customer': type_of_customer, 'recommended action': val}


@app.route('/')
def home():
    """
    mehtod for rendering the HTML GUI
    """
    return render_template('index.html')


@app.route('/analyse', methods=['POST'])
def analyse():
    """
    method for analysing the customer behavior and displaying the results
    
    """
    customer_id = request.form.get("CustomerId")
    customer_info = get_customer_insights(int(customer_id))
    if not customer_info:
        return Response('Could not analyse the entered customer ID. Please try with another cutomer ID.', status=404)
    return render_template('index.html',
                           type_of_customer='Type of customer: {}'.format(customer_info['Type of customer']),
                           recommended_action='Recommended action: {}'.format(customer_info['recommended action']))


if __name__ == "__main__":
    app.run(debug=True)
