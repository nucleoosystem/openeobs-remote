from . import observation_report_helpers as helpers
from bs4 import BeautifulSoup
from datetime import datetime
import json


class TestObservationReportRendering(helpers.ObservationReportHelpers):

    def test_01_report_header_structure(self):
        """
        Test that the report header is rendering correctly with the patient
        name on the left and the hospital logo on the right
        """
        report_data = {
            'spell_id': 1,
            'start_date': None,
            'end_date': None,
            'ews_only': True
        }
        report_obj = self.registry(self.report_model)
        report_html = report_obj.render_html(
            self.cr, self.uid, [], data=report_data, context=None)
        beautiful_report = BeautifulSoup(report_html, 'html.parser')
        header_name = beautiful_report.select('.header .col-xs-9 h2')[0]
        self.assertEqual(
            header_name.string,
            'Test Patient',
            'Report header name is incorrect'
        )
        header_image = beautiful_report.select('.header .col-xs-3 img')[0]
        self.assertEqual(
            header_image['src'],
            'data:image/png;base64,{0}'.format(self.test_logo),
            'Report logo is incorrect'
        )

    def test_02_report_footer_structure(self):
        """
        Test that the report footer is rendering correctly with the user name,
        print date in HH:MM dd/mm/yy, hospital name and patient NHS number
        """
        report_data = {
            'spell_id': 1,
            'start_date': None,
            'end_date': None,
            'ews_only': True
        }
        report_obj = self.registry(self.report_model)
        report_html = report_obj.render_html(
            self.cr, self.uid, [], data=report_data, context=None)
        beautiful_report = BeautifulSoup(report_html, 'html.parser')
        footer_info = beautiful_report.select('.footer .col-xs-9 p')[0]
        footer_image = footer_info.select('img')[0]
        footer_info = footer_info.text
        footer_has_name = 'Administrator' in footer_info
        date_string = datetime.now().strftime('%H:%M %d/%m/%y')
        footer_has_print_date = date_string in footer_info
        footer_has_hosp_name = 'Test Hospital' in footer_info
        footer_has_nhs_number = 'NHS1234123' in footer_info
        self.assertTrue(footer_has_name, 'Incorrect name in footer')
        self.assertTrue(footer_has_print_date, 'Incorrect date in footer')
        self.assertTrue(footer_has_hosp_name, 'Incorrect hosp name in footer')
        self.assertTrue(footer_has_nhs_number, 'Incorrect NHS num in footer')
        self.assertEqual(
            footer_image['src'],
            '/nh_eobs/static/src/img/open_eobs_logo.png',
            'Incorrect logo image linked to in footer'
        )
        self.assertEqual(
            footer_image['alt'],
            'Open-eObs',
            'Incorrect alt tag for footer image'
        )

    def test_03_report_page_structure(self):
        """
        Test that the report page structure is correct with the first page
        containing the patient details and graph and the other pages with data
        tables
        """
        report_data = {
            'spell_id': 1,
            'start_date': None,
            'end_date': None,
            'ews_only': True
        }
        report_obj = self.registry(self.report_model)
        report_html = report_obj.render_html(
            self.cr, self.uid, [], data=report_data, context=None)
        beautiful_report = BeautifulSoup(report_html, 'html.parser')
        rows = beautiful_report.select('.page div.row')
        self.assertGreater(len(rows), 3, 'Incorrect number of rows found')

    def test_04_report_first_page_details_structure(self):
        """
        Test that the details on the front page are in the correct structure
        """
        report_data = {
            'spell_id': 1,
            'start_date': None,
            'end_date': None,
            'ews_only': True
        }
        report_obj = self.registry(self.report_model)
        report_html = report_obj.render_html(
            self.cr, self.uid, [], data=report_data, context=None)
        beautiful_report = BeautifulSoup(report_html, 'html.parser')
        rows = beautiful_report.select('.page div.row')
        report_title_div = rows[0]
        report_title = report_title_div.select('h1')[0]
        self.assertEqual(
            report_title.string,
            'Patient Observation Report',
            'Incorrect report title'
        )
        patient_details_div = rows[1]
        patient_details_headers = patient_details_div.select('h2')
        patient_details = patient_details_headers[0]
        hospital_details = patient_details_headers[1]
        self.assertEqual(
            patient_details.string,
            'Patient',
            'Incorrect patient details'
        )
        self.assertEqual(
            hospital_details.string,
            'Hospital Visit',
            'Incorrect hospital details'
        )

    def test_05_report_first_page_chart_structure(self):
        """
        Test that the chart on the front page is in the correct structure
        """
        report_data = {
            'spell_id': 1,
            'start_date': None,
            'end_date': None,
            'ews_only': True
        }
        report_obj = self.registry(self.report_model)
        report_html = report_obj.render_html(
            self.cr, self.uid, [], data=report_data, context=None)
        beautiful_report = BeautifulSoup(report_html, 'html.parser')
        rows = beautiful_report.select('.page div.row')
        patient_chart_div = rows[2]
        patient_chart = patient_chart_div.select('#chart')[0]
        scripts = patient_chart_div.select('script')
        dthree = scripts[0]
        graphlib = scripts[1]
        data = scripts[2]
        obs_report_script = scripts[3]
        self.assertEqual(
            patient_chart['style'],
            'width: 825px; height: 885px;',
            'Incorrect chart dimensions'
        )
        self.assertEqual(
            dthree['src'],
            '/nh_graphs/static/lib/js/d3.js',
            'Incorrect d3.js script'
        )
        self.assertEqual(
            graphlib['src'],
            '/nh_graphs/static/src/js/nh_graphlib.js',
            'Incorrect graphlib script'
        )
        data_as_json = data.text.replace('var obs_data = ', '')\
            .replace(';', '')
        json_data = json.loads(data_as_json)[0]
        for key, value in json_data.iteritems():
            if key in ['create_date', 'date_started', 'date_terminated',
                       'write_date']:
                json_data[key] = datetime.strptime(
                    value,
                    '%a %b %d %Y %H:%M:%S %Z'
                ).strftime('%Y-%m-%d %H:%M:%S')
        del json_data['o2_target']
        self.assertEqual(
            json_data,
            self.ews_values,
            'Incorrect chart data'
        )
        self.assertEqual(
            obs_report_script['src'],
            '/nh_eobs/static/src/js/observation_report.js',
            'Incorrect Observation Report JavaScript'
        )

    def test_06_ews_only_shows_only_ews_table(self):
        """
        Test that the EWS only chart shows only EWS data in the table and no
        other observations
        """
        report_data = {
            'spell_id': 1,
            'start_date': None,
            'end_date': None,
            'ews_only': True
        }
        report_obj = self.registry(self.report_model)
        report_html = report_obj.render_html(
            self.cr, self.uid, [], data=report_data, context=None)
        beautiful_report = BeautifulSoup(report_html, 'html.parser')
        table_section_headers = beautiful_report.select('h3')
        self.assertEqual(
            len(table_section_headers),
            3,
            'Incorrect number of tables'
        )
        ews_values_header = table_section_headers[0]
        monitoring_header = table_section_headers[1]
        actions_header = table_section_headers[2]
        self.assertEqual(
            ews_values_header.text,
            'NEWS Values',
            'Incorrect NEWS table header'
        )
        self.assertEqual(
            monitoring_header.text,
            'Patient Monitoring Exceptions',
            'Incorrect Monitoring table header'
        )
        self.assertEqual(
            actions_header.text,
            'Actions Triggered',
            'Incorrect Actions table header'
        )
