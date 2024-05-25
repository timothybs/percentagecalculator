import os
from flask import Flask, render_template, request, session, redirect, url_for
import math

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'calculate_percentage' in request.form:
            try:
                base = float(request.form.get("base", ""))
                percentage = float(request.form.get("percentage", ""))
                session['percentage_result'] = (percentage / 100) * base
            except ValueError:
                session['percentage_result'] = "Please enter valid numbers for the percentage calculator"

        elif 'calculate_cloud_base' in request.form:
            try:
                surface_temp = float(request.form.get("surface_temp", ""))
                dew_point = float(request.form.get("dew_point", ""))
                unit = request.form.get("unit", "C")
                convert_to_meters = 'convert_to_meters' in request.form

                if unit == "F":
                    cloud_base_result = abs((surface_temp - dew_point) / 4.4) * 1000
                else:  # Default to Celsius
                    cloud_base_result = abs((surface_temp - dew_point) / 2.5) * 1000

                if convert_to_meters:
                    cloud_base_result = cloud_base_result * 0.3048  # Convert feet to meters

                cloud_base_result = round(cloud_base_result)  # Round to no decimal places

                session['cloud_base_result'] = cloud_base_result
                session['convert_to_meters'] = convert_to_meters

            except ValueError:
                session['cloud_base_result'] = "Please enter valid numbers for the cloud base calculator"

        elif 'calculate_sales_price' in request.form:
            try:
                cost_price = float(request.form.get("cost_price", ""))
                margin = float(request.form.get("margin", ""))
                tax_percentage = float(request.form.get("tax_percentage", 20))  # Default to 20%
                rounding = 'rounding' in request.form

                margin_amount = cost_price * (margin / 100)
                pre_tax_amount = cost_price + margin_amount
                tax_amount = pre_tax_amount * (tax_percentage / 100)
                sales_price = pre_tax_amount + tax_amount

                if rounding:
                    sales_price = math.ceil(sales_price) - 0.05

                session['sales_price_result'] = sales_price

            except ValueError:
                session['sales_price_result'] = "Please enter valid numbers for the sales price calculator"
        
        return redirect(url_for('index'))

    # Retrieve results from session or set to None if not available
    percentage_result = session.pop('percentage_result', None)
    cloud_base_result = session.pop('cloud_base_result', None)
    sales_price_result = session.pop('sales_price_result', None)
    convert_to_meters = session.pop('convert_to_meters', False)

    return render_template("index.html", 
                           percentage_result=percentage_result, 
                           cloud_base_result=cloud_base_result,
                           sales_price_result=sales_price_result,
                           convert_to_meters=convert_to_meters)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))  # Changed port to 8000
    app.run(host='0.0.0.0', port=port, debug=True)

