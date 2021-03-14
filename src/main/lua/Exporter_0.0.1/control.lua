function get_blueprint_xy(blueprint)
    local x
    local y

    for _, ent in pairs(blueprint.get_blueprint_entities()) do
        local prots = game.get_filtered_entity_prototypes{{ filter = "name", name = ent.name }}

        local entity_x = math.floor(ent.position.x + prots[ent.name].selection_box.left_top.x)
        local entity_y = math.floor(ent.position.y + prots[ent.name].selection_box.left_top.y)

        x = math.min(x or entity_x, entity_x)
        y = math.min(y or entity_y, entity_y)
    end

    -- Because of rails alignment
    x = x - (x % 2)
    y = y - (y % 2)

    return x, y
end

function move_blueprint(blueprint, x, y)
    local entities = blueprint.get_blueprint_entities()

    for _, ent in pairs(entities) do
        ent.position.x = ent.position.x + x
        ent.position.y = ent.position.y + y
    end

    blueprint.set_blueprint_entities(entities)
end

function blueprint_save(name, bp_x, bp_y, bp_x_offset)
    local player = game.players[1]
    local blueprint = player.cursor_stack
    
    blueprint.set_stack("blueprint")
    blueprint.create_blueprint{
        area = {
            { bp_x, bp_y },
            { bp_x + 10, bp_y + (3 * 32) + (2 * 12) }
        },
        surface = player.surface,
        force = player.force,
        include_station_names = true,
    }

    x, y = get_blueprint_xy(blueprint)
    move_blueprint(blueprint, -(x + bp_x_offset), -y)

    blueprint.blueprint_snap_to_grid = {0, 0}
    blueprint.blueprint_absolute_snapping = true

    bp_string = blueprint.export_stack()
    blueprint.set_stack()

    game.write_file(name, bp_string)
end

function export_blueprints()
    local x
    local y = -748

    x = -352
    blueprint_save('station_in_item.blueprint', x, y, 0)
    blueprint_save('station_in_fluid.blueprint', x + 10, y, 0)

    x = -212
    blueprint_save('station_out_item.blueprint', x, y, -2)
    blueprint_save('station_out_fluid.blueprint', x + 10, y, -2)

    game.print("Blueprints exported")
end

script.on_event(
    "export-blueprints",
    function(event)
        return export_blueprints()
    end
)
