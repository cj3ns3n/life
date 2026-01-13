import pyglet

class InfoText():
    green = (0, 255, 0, 255)
    blue = (0, 0, 128, 255)
    white = (255, 255, 255, 255)
    initial_y_loc = 280  # Start from top of window (adjust based on window height)

    def __init__(self):
        # Pyglet labels will be created on-demand during blit
        self.labels = []
        self.display_count = 0
        self.entity = None
        self.rect_x = 0
        self.rect_y = 0
        self.rect_width = 0
        self.rect_height = 0
    # end def

    def blit(self, batch, stats_container):
        """Create Pyglet labels for stats overlay. Returns list of labels to draw."""
        y_loc = self.initial_y_loc
        self.labels = []
        stats = stats_container.get_stats()
        x_loc = 10
        max_width = 0

        # Cycles
        label = pyglet.text.Label(
            'Cycles %d' % stats['cycles'],
            font_name='Arial',
            font_size=14,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Population
        pop_text_str = 'Population %03d; Males %03d; Females %03d' % (
            stats['births'] - stats['maternal_deaths'] - stats['natural_deaths'], 
            stats['males'], 
            stats['females']
        )
        label = pyglet.text.Label(
            pop_text_str,
            font_name='Arial',
            font_size=14,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Births and deaths
        births = stats['births']
        m_deaths = stats['maternal_deaths']
        n_deaths = stats['natural_deaths']
        m_deathrate = 100.0 * float(m_deaths) / float(births) if births > 0 else 0.0
        births_text_str = 'Births: %02d; (birth rate: %0.1f) Maternal Deaths: %02d (rate: %0.1f%%); Natural Deaths: %02d (death rate: %0.1f%%)' % (
            births, stats['birth_rate']*100, m_deaths, m_deathrate, n_deaths, stats['death_rate']*100
        )
        label = pyglet.text.Label(
            births_text_str,
            font_name='Arial',
            font_size=12,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Age stats
        label = pyglet.text.Label(
            'Avg Age: %.1f, Stdv Age: %.1f' % (stats['age_avg'], stats['age_stdev']),
            font_name='Arial',
            font_size=14,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Health stats
        label = pyglet.text.Label(
            'Avg Health: %.1f, Stdv Health: %.1f' % (stats['health_avg'], stats['health_stdev']),
            font_name='Arial',
            font_size=14,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Size stats
        label = pyglet.text.Label(
            'Avg Size: %.1f, Stdv Size: %.1f' % (stats['size_avg'], stats['size_stdev']),
            font_name='Arial',
            font_size=14,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Display refreshes
        label = pyglet.text.Label(
            'Refreshes %d' % stats['display_iterations'],
            font_name='Arial',
            font_size=14,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Entity info
        entity_text = self.get_entity_text()
        label = pyglet.text.Label(
            entity_text,
            font_name='Arial',
            font_size=14,
            x=x_loc, y=y_loc,
            color=InfoText.white,
            anchor_x='left', anchor_y='top',
            batch=batch
        )
        self.labels.append(label)
        y_loc -= 20
        max_width = max(max_width, label.content_width)

        # Update rect dimensions
        height = y_loc - InfoText.initial_y_loc
        self.rect_x = x_loc
        self.rect_y = InfoText.initial_y_loc
        self.rect_width = max_width
        self.rect_height = height
        
        return self.labels
    # end def

    def get_rect(self):
        """Returns a tuple (x, y, width, height) for compatibility."""
        return (self.rect_x, self.rect_y, self.rect_width, self.rect_height)
    # end def

    def set_entity(self, entity, entity_pos):
        self.entity = entity
        self.entity_pos = entity_pos

    def get_entity_text(self):
        entity_text = 'Entity: None'
        if self.entity:
            entity_text = 'Entity: %s %s' % (str(self.entity_pos), str(self.entity))
        return entity_text
    # end def
# end class
