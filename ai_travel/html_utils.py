
# import datetime
from datetime import datetime

def generate_html_table(table_data) -> str:
    """
    Generate an HTML table from the provided data.

    Args:
        table_data (list of dict): List of dictionaries containing travel data. Each dictionary should have keys:
            'City', 'Arrival Time', 'Distance (km)', 'Weather'.
    """
    # Center justify the Distance (km) column by updating the <th> and <td> styles
    html_table = """
        <table class='travel-table' style="
            border-collapse: collapse;
            width: 100%;
            font-family: Arial, sans-serif;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <thead style="
                background-color: #f4f6fa;
                color: #333;
                font-weight: bold;
            ">
                <tr>
                    <th style="border: 1px solid #ddd; padding: 10px 16px; text-align: center;">City</th>
                    <th style="border: 1px solid #ddd; padding: 10px 16px; text-align: center;">Arrival Time</th>
                    <th style="border: 1px solid #ddd; padding: 10px 16px; text-align: center;">Distance (km)</th>
                    <th style="border: 1px solid #ddd; padding: 10px 16px; text-align: center;">Weather</th>
                </tr>
            </thead>
            <tbody>
            
    """    
    
    for row in table_data:
        html_table += "<tr>"
        html_table += f"<td style='text-align: center;'>{row['City']}</td>"
        arrival_dt = datetime.fromisoformat(row['Arrival Time'])
        formatted_arrival = arrival_dt.strftime('%I:%M %p, %A, %d %B %Y')
        html_table += f"<td style='text-align: center;'>{formatted_arrival}</td>"
        html_table += f"<td style='text-align: center;'>{row['Distance (km)']}</td>"
        html_table += f"<td style='text-align: center;'>{row['Weather']}</td>"
        html_table += "</tr>"

    html_table += """
        </tbody>
    </table>
    """
    return html_table