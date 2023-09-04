from unittest import mock

from constants import PayType, RollResultCode


class TestPlayer:
    def test_roll_die(self, mock_player):
        roll_1, roll_2 = mock_player.roll_die()
        assert 1 <= roll_1 <= 6
        assert 1 <= roll_2 <= 6

    @mock.patch("requests.patch", return_value=None)
    def test_roll(self, mock_patch, mock_player):
        roll = mock_player.roll()
        assert 2 <= roll <= 12

    @mock.patch("schemas.player.Player.roll_die")
    @mock.patch("requests.patch", return_value=None)
    def test_roll_third_double(self, mock_patch, mock_roll_die, mock_player):
        mock_roll_die.return_value = (2, 2)
        mock_player.roll_1 = False
        mock_player.roll_2 = True
        mock_player.roll_3 = True
        result = mock_player.roll()
        assert result == RollResultCode.THIRD_DOUBLE

    @mock.patch("schemas.player.Player.roll_die")
    @mock.patch("requests.patch", return_value=None)
    def test_roll_jail_double(self, mock_patch, mock_roll_die, mock_jailed_player):
        mock_roll_die.return_value = (2, 2)
        mock_jailed_player.roll_1 = False
        mock_jailed_player.roll_2 = False
        mock_jailed_player.roll_3 = False
        result = mock_jailed_player.roll()
        assert result == RollResultCode.JAIL_DOUBLE

    @mock.patch("schemas.player.Player.roll_die")
    @mock.patch("requests.patch", return_value=None)
    def test_roll_stay_in_jail(self, mock_patch, mock_roll_die, mock_jailed_player):
        mock_roll_die.return_value = (2, 1)
        mock_jailed_player.roll_1 = False
        mock_jailed_player.roll_2 = False
        mock_jailed_player.roll_3 = False
        result = mock_jailed_player.roll()
        assert result == 0
        assert mock_jailed_player.in_jail is True
        assert mock_jailed_player.jail_count == 1

    def test_pay(self, mock_player):
        with mock.patch("requests.patch", return_value=None):
            mock_player.pay(100, PayType.RENT)
            assert mock_player.cash == 1400

    def test_pay_insufficient_funds(self, mock_player):
        with mock.patch("requests.patch", return_value=None):
            mock_player.pay(2000, PayType.RENT)
            assert mock_player.cash == 0

    def test_pay_income_tax_choice_1(self, mock_player):
        with mock.patch("click.prompt", return_value=1), mock.patch(
            "requests.patch", return_value=None
        ):
            mock_player.pay_income_tax()
            assert mock_player.cash == 1300

    def test_pay_income_tax_choice_2(self, mock_player):
        with mock.patch("click.prompt", return_value=2), mock.patch(
            "requests.patch", return_value=None
        ):
            mock_player.pay_income_tax()
            assert mock_player.cash == 1350

    def test_handle_draw_card_gooj(self, mock_gooj_card, mock_player):
        mock_player.handle_draw_card(mock_gooj_card)
        pass

    def test_handle_draw_chance(self, mock_chance_card, mock_player):
        mock_player.handle_draw_card(mock_chance_card)
        pass

    def test_handle_draw_cc(self, mock_cc_card, mock_player):
        mock_player.handle_draw_card(mock_cc_card)
        pass

    def test_player_str(self, mock_gamespace_no_deed, mock_player):
        mock_player.properties.append(mock_gamespace_no_deed)
        assert mock_player.__str__() == "Cash: $1500, Properties(group): [test(None)]"
