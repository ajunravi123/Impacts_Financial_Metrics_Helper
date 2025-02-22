function showToast(message, type = 'error') {
    const toastContainer = document.getElementById('toastContainer');
    
    const popup = document.createElement('div');
    popup.className = 'fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50';
    
    const popupContent = document.createElement('div');
    popupContent.className = `popup p-6 rounded-lg shadow-xl text-white max-w-sm w-full bg-gradient-to-br ${
        type === 'error' ? 'from-gray-700 to-blue-900' : 'from-green-700 to-teal-900'
    } border border-gray-600`;
    
    const messageText = document.createElement('p');
    messageText.className = 'text-lg mb-4 text-shadow';
    messageText.textContent = message;
    popupContent.appendChild(messageText);
    
    const closeButton = document.createElement('button');
    closeButton.className = 'bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition duration-300 font-semibold';
    closeButton.textContent = 'Close';
    closeButton.addEventListener('click', () => {
        popup.remove();
    });
    popupContent.appendChild(closeButton);
    
    popup.appendChild(popupContent);
    toastContainer.appendChild(popup);
}

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const input = document.getElementById('tickerInput').value.trim();
    if (!input) {
        showToast('Please enter a company name or ticker');
        return;
    }

    const loader = document.getElementById('loader');
    const results = document.getElementById('results');
    loader.classList.remove('hidden');
    results.classList.add('hidden');

    try {
        const response = await fetch(`/analyze/${encodeURIComponent(input)}`);
        if (!response.ok) throw new Error('Analysis failed');
        const data = await response.json();

        if (data.error) {
            showToast(data.error);
        } else {
            const tableBody = document.querySelector('#resultsTable tbody');
            tableBody.innerHTML = '';
            const benefits = data.benefits;

            // Calculate sums for low and high
            let sumLow = 0;
            let sumHigh = 0;
            const metricsToSum = [
                'Margin_Rate_Lift',
                'Margin_on_Revenue_Lift',
                'Efficiency_Re_Investment',
                'Reduction_in_Xfer_Expenses',
                'Inventory_Carrying_Costs'
            ];

            // Populate table and accumulate sums
            for (const [metric, values] of Object.entries(benefits)) {
                const row = document.createElement('tr');
                const lowValue = typeof values.low === 'number' ? values.low : 0; // Treat "Not Available" as 0 for summing
                const highValue = typeof values.high === 'number' ? values.high : 0;

                row.innerHTML = `
                    <td>${metric.replace(/_/g, ' ')}</td>
                    <td>$${lowValue.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
                    <td>$${highValue.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
                `;
                tableBody.appendChild(row);

                // Add to sums if metric is in the list
                if (metricsToSum.includes(metric)) {
                    sumLow += lowValue;
                    sumHigh += highValue;
                }
            }

            // Add total row
            const totalRow = document.createElement('tr');
            totalRow.className = 'font-bold bg-gray-600'; // Highlight total row
            totalRow.innerHTML = `
                <td>Total Benefit</td>
                <td>$${sumLow.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
                <td>$${sumHigh.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
            `;
            tableBody.appendChild(totalRow);

            // Populate summary
            const summaryList = document.getElementById('summary');
            summaryList.innerHTML = '';
            let printing_class = 'noclass';
            data.summary.split('\n').filter(line => line.trim()).forEach(line => {
                const li = document.createElement('div');
                let line_data = line.replace(/^- /, '');
                li.textContent = line_data;
                if(line_data == "Raw Data:" || line_data == "Raw Data Summary:"){
                    printing_class = "raw_div";
                }else if(line_data == "Calculated Benefits:"){
                    printing_class = "calc_div";
                }
                
                li.classList.add(printing_class);
                summaryList.appendChild(li);
            });

            results.classList.remove('hidden');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`);
    } finally {
        loader.classList.add('hidden');
    }
});