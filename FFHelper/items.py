from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, Join


class PlayerItem(Item):
    
    name = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor=Join(),
            )
    player_url = Field()
    position = Field(
            input_processor=MapCompose(unicode.strip, unicode.upper),
            output_processor=Join(),
            )
    age = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor=Join(),
            )
    
    current_team = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor=Join(),
            )
    team_one_year_ago = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor=Join(),
            )
    team_two_year_ago = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor=Join(),
            )
    team_three_year_ago = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor=Join(),
            )
    
    points_one_year_ago = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor= Join(),
            )
    points_two_year_ago = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor= Join(),
            )
    points_three_year_ago = Field(
            input_processor=MapCompose(unicode.strip),
            output_processor= Join(),
            )