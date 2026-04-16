% Buenos Aires Restaurant Expert System - Knowledge Base
% Preserving original dataset with added wildcard matching logic.

% restaurant(Name, Cuisine, Budget, SameArea, Neighborhood, Dietary, Vibe, Distance, Time, Reservation).
restaurant(santos_manjares, argentine, medium, yes, centro, none, casual, walk, lunch_dinner, no).
restaurant(el_mirasol, argentine, high, yes, retiro, none, romantic_family, walk, dinner, recommended).
restaurant(don_julio, argentine, luxury, no, palermo, none, romantic_trendy, uber, dinner, yes).
restaurant(la_cabrera, argentine, high, no, palermo, none, trendy_social, uber, dinner, yes).
restaurant(el_desnivel, argentine, low, no, san_telmo, none, casual_local, uber, lunch_dinner, no).
restaurant(parrilla_pena, argentine, medium, yes, centro, none, local, walk, lunch, no).
restaurant(mr_cook, empanadas, low, yes, centro, none, quick, walk, lunch_snack, no).
restaurant(el_hornero, empanadas, low, no, palermo, none, casual, uber, lunch, no).
restaurant(chori, street_food, low, no, palermo, none, trendy, uber, lunch_dinner, no).
restaurant(dogg, fast_food, low, yes, centro, none, quick, walk, late, no).
restaurant(saint_moritz, italian, low, yes, centro, none, family_casual, walk, lunch_dinner, no).
restaurant(punto, italian, medium, yes, centro, none, relaxed, walk, dinner, no).
restaurant(il_ballo_del_mattone, italian, medium, no, palermo, none, romantic, uber, dinner, yes).
restaurant(siamo_nel_forno, italian, medium, no, palermo, none, trendy, uber, lunch_dinner, no).
restaurant(toki, asian, medium, no, palermo, none, trendy_social, uber, dinner, recommended).
restaurant(kuro, asian, high, no, palermo, none, romantic, uber, dinner, yes).
restaurant(nicky_ny_sushi, asian, high, no, palermo, none, upscale, uber, dinner, yes).
restaurant(osaka, asian, luxury, no, palermo, none, luxury, uber, dinner, yes).
restaurant(craft_vegan_bakery, vegan, medium, no, recoleta, vegan, casual, uber, breakfast_lunch, no).
restaurant(gout_gluten_free, cafe, medium, no, recoleta, gluten_free, casual, uber, breakfast_lunch, no).
restaurant(buenos_aires_verde, vegan, high, no, palermo, vegan, upscale, uber, dinner, yes).
restaurant(hierbabuena, vegetarian, medium, no, san_telmo, vegetarian, relaxed, uber, lunch, no).
restaurant(rapanui_retiro, dessert, medium, yes, retiro, none, casual, walk, dessert_late, no).
restaurant(cadore, dessert, medium, yes, centro, none, casual, walk, dessert, no).
restaurant(cafe_tortoni, cafe, medium, yes, centro, none, cultural, walk, breakfast_lunch, no).
restaurant(full_city_coffee, cafe, medium, no, palermo, none, study_trendy, uber, breakfast_lunch, no).

% Helper Rules for Matching with Wildcards

cuisine_match(any, _).
cuisine_match(C, C).

budget_match(any, _).
budget_match(B, B).

% same_area logic: if yes, must be yes. if no, don't care about RSameArea, but we'll check neighborhood later.
same_area_match(yes, yes).
same_area_match(no, _).

dietary_match(any, _).
dietary_match(none, _).
dietary_match(vegetarian, vegetarian).
dietary_match(vegan, vegan).
dietary_match(celiac, gluten_free).
dietary_match(halal, halal).

% Vibe matches (supports specific categories matching sub-vibes)
vibe_match(any, _).
vibe_match(casual, V) :- member(V, [casual, casual_local, family_casual, quick, local, relaxed, cultural]).
vibe_match(romantic, V) :- member(V, [romantic, romantic_family, romantic_trendy, upscale, luxury]).
vibe_match(family, V) :- member(V, [family_casual, romantic_family, casual]).
vibe_match(trendy, V) :- member(V, [trendy, trendy_social, romantic_trendy, study_trendy, upscale, luxury]).

distance_match(any, _).
distance_match(walking, walk).
distance_match(short_uber, _).

time_match(any, _).
time_match(breakfast, breakfast_lunch).
time_match(lunch, V) :- member(V, [lunch, lunch_dinner, lunch_snack, breakfast_lunch]).
time_match(dinner, V) :- member(V, [dinner, lunch_dinner]).
time_match(late_night, V) :- member(V, [late, dessert_late]).

reservation_match(no_preference, _).
reservation_match(yes, V) :- member(V, [yes, recommended]).
reservation_match(no, no).

% Main Recommendation Rule
recommend(Name, UNbh, UCuis, UBudg, USame, UDiet, UVibe, UDist, UTime, URes) :-
    restaurant(Name, RCuis, RBudg, RSame, RNbh, RDiet, RVibe, RDist, RTime, RRes),
    cuisine_match(UCuis, RCuis),
    budget_match(UBudg, RBudg),
    same_area_match(USame, RSame),
    (
        USame = yes
        ;
        USame = no, RNbh = UNbh
    ),
    dietary_match(UDiet, RDiet),
    vibe_match(UVibe, RVibe),
    distance_match(UDist, RDist),
    time_match(UTime, RTime),
    reservation_match(URes, RRes).
