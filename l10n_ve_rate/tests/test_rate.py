import logging
from odoo import fields
from odoo.tests import TransactionCase, tagged
from odoo.tools import float_round

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install", "l10n_ve_rate")
class TestResCurrencyRate(TransactionCase):
    def _setup_main_company(self):
        self.company_vef = self.env["res.company"].create(
            {
                "name": "Company VEF",
                "currency_id": self.currency_vef.id,
                "currency_foreign_id": self.currency_usd.id,
            }
        )

        self.env["res.currency.rate"].create(
            {
                "name": fields.Date.from_string("2025-07-28"),
                "currency_id": self.currency_usd.id,
                "inverse_company_rate": 120.439,
                "company_id": self.company_vef.id,
            }
        )

        self.env["res.currency.rate"].create(
            {
                "name": fields.Date.from_string("2025-07-21"),
                "currency_id": self.currency_usd.id,
                "inverse_company_rate": 119.439,
                "company_id": self.company_vef.id,
            }
        )
        self.env["res.currency.rate"].create(
            {
                "name": fields.Date.from_string("2025-07-18"),
                "currency_id": self.currency_usd.id,
                "inverse_company_rate": 118.439,
                "company_id": self.company_vef.id,
            }
        )

    def _setup_2nd_company(self):
        self.company_usd = self.env["res.company"].create(
            {
                "name": "Company USD",
                "currency_id": self.currency_usd.id,
                "currency_foreign_id": self.currency_vef.id,
            }
        )

        self.env["res.currency.rate"].create(
            {
                "name": fields.Date.from_string("2025-07-28"),
                "currency_id": self.currency_vef.id,
                "company_rate": 120.439,
                "company_id": self.company_usd.id,
            }
        )

        self.env["res.currency.rate"].create(
            {
                "name": fields.Date.from_string("2025-07-21"),
                "currency_id": self.currency_vef.id,
                "company_rate": 119.439,
                "company_id": self.company_usd.id,
            }
        )
        self.env["res.currency.rate"].create(
            {
                "name": fields.Date.from_string("2025-07-18"),
                "currency_id": self.currency_vef.id,
                "company_rate": 118.439,
                "company_id": self.company_usd.id,
            }
        )

    def setUp(self):
        super().setUp()
        self.currency_usd = self.env.ref("base.USD")
        self.currency_vef = self.env.ref("base.VEF")
        self._setup_main_company()
        self._setup_2nd_company()


    def test_date_up_to_last_rate(self):
        """
        Test that the method returns the last rate before or on the given date.
        """
        rate_vef = (
            self.env["res.currency.rate"]
            .with_company(self.company_vef)
            .compute_rate(
                foreign_currency_id=self.currency_usd.id,
                rate_date=fields.Date.from_string("2025-07-29"),
            )
        )
        rate_usd = (
            self.env["res.currency.rate"]
            .with_company(self.company_usd)
            .compute_rate(
                foreign_currency_id=self.currency_vef.id,
                rate_date=fields.Date.from_string("2025-07-29"),
            )
        )
        self.assertEqual(
            float_round(rate_vef["foreign_rate"], precision_digits=3), 120.439, "Rate should be 120.439 for 2025-07-29"
        )

        self.assertEqual(
            float_round(rate_usd["foreign_rate"], precision_digits=3), 120.439, "Rate should be 120.439 for 2025-07-29"
        )

    def test_date_before_to_first_rate(self):
        """
        Test that the method returns the first rate that is after the given date
        if theres not rate in that date or before.
        """
        rate_vef = (
            self.env["res.currency.rate"]
            .with_company(self.company_vef)
            .compute_rate(
                foreign_currency_id=self.currency_usd.id,
                rate_date=fields.Date.from_string("2025-07-17"),
            )
        )

        rate_usd = (
            self.env["res.currency.rate"]
            .with_company(self.company_usd)
            .compute_rate(
                foreign_currency_id=self.currency_vef.id,
                rate_date=fields.Date.from_string("2025-07-17"),
            )
        )

        self.assertEqual(
            float_round(rate_vef["foreign_rate"], precision_digits=3), 118.439, "Rate should be 118.439 for 2025-07-17"
        )

        self.assertEqual(
            float_round(rate_usd["foreign_rate"], precision_digits=3), 118.439, "Rate should be 118.439 for 2025-07-17"
        )

    def test_date_equal_to_a_rate_date(self):
        """
        Test that the method returns the rate that is in the given date.
        """
        rate_vef = (
            self.env["res.currency.rate"]
            .with_company(self.company_vef)
            .compute_rate(
                foreign_currency_id=self.currency_usd.id,
                rate_date=fields.Date.from_string("2025-07-21"),
            )
        )

        rate_usd = (
            self.env["res.currency.rate"]
            .with_company(self.company_usd)
            .compute_rate(
                foreign_currency_id=self.currency_vef.id,
                rate_date=fields.Date.from_string("2025-07-21"),
            )
        )
        self.assertEqual(
            float_round(rate_vef["foreign_rate"], precision_digits=3), 119.439, "Rate should be 119.439 for 2025-07-21"
        )

        self.assertEqual(
            float_round(rate_usd["foreign_rate"], precision_digits=3), 119.439, "Rate should be 119.439 for 2025-07-21"
        )
