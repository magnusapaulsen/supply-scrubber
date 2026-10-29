import pdf_generator
import calculate_total
import apartment_summary
import wash_summary


def test_calculate_total_rounds_totals_to_two_decimals():
    washes = [{'Items': {'Coffee': 2}, 'Guests': {}}]
    result = calculate_total.calculate_total(washes, {'Coffee': 33.333})
    assert result[0]['Items']['Total'] == 66.67


def test_calculate_total_computes_guest_totals():
    washes = [{'Items': {}, 'Guests': {'Amount of Guests': 3}}]
    result = calculate_total.calculate_total(washes, {'Amount of Guests': 75.0})
    assert result[0]['Guests']['Total'] == 225.0


def test_group_by_name_merges_washes_per_apartment():
    washes = [
        {'Name': 'Apt 1', 'Address': 'Street 1', 'Task': 'Deep clean', 'Date': '2026-10-01', 'Items': {'Toilet paper': 2}, 'Guests': {'Amount of Guests': 2}},
        {'Name': 'Apt 1', 'Address': 'Street 1', 'Task': 'Deep clean', 'Date': '2026-10-02', 'Items': {'Toilet paper': 1}, 'Guests': {'Amount of Guests': 1}},
        {'Name': 'Apt 2', 'Address': 'Street 2', 'Task': 'Deep clean', 'Date': '2026-10-01', 'Items': {'Toilet paper': 5}, 'Guests': {'Amount of Guests': 4}},
    ]
    grouped = apartment_summary.group_by_name(washes)
    assert grouped['Apt 1']['Items']['Toilet paper'] == 3
    assert grouped['Apt 2']['Items']['Toilet paper'] == 5


def test_finalize_data_sets_wash_totals():
    apartments = {'Apt 1': {'Items': {'Total': 10.0}, 'Guests': {'Total': 5.0}}}
    finalized = wash_summary.finalize_data(apartments, {'Apt 1': 2}, {'Apt 1': 580})
    assert finalized['Apt 1']['Washes']['Price'] == 580
    assert finalized['Apt 1']['Washes']['Quantity'] == 2
    assert finalized['Apt 1']['Washes']['Total'] == 1160


def test_finalize_data_ignores_unknown_apartments():
    finalized = wash_summary.finalize_data({'Apt 1': {}}, {'Unknown Apt': 2}, {'Unknown Apt': 100})
    assert finalized == {'Apt 1': {}}


def test_generate_pdf_creates_report(tmp_path):
    data = {
        'Apt 1': {
            'Items': {'Toilet paper': 2, 'Total': 11.0},
            'Guests': {'Amount of Guests': 2, 'Total': 150.0},
        }
    }
    out_path = tmp_path / 'report.pdf'
    pdf_generator.generate_pdf(data, str(out_path))
    assert out_path.exists()
