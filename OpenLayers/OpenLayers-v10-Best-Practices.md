# OpenLayers v10 Best Practices

> Project guidance for building maintainable, performant OpenLayers
> applications.

## Core Principles

-   Treat OpenLayers as a rendering and interaction engine, not the
    application's state store.
-   Keep business logic outside OpenLayers classes.
-   Separate domain models from OpenLayers `Feature` objects.
-   Prefer composition over subclassing OpenLayers classes.
-   Keep rendering concerns isolated from application concerns.

## Map

-   Create a single `Map` instance unless multiple maps are a deliberate
    requirement.
-   Reuse a single `View` for the lifetime of the map.
-   Dispose of the map when it is no longer required.
-   Avoid recreating the map to apply configuration changes.
-   Configure controls and interactions explicitly.

## Layers

-   Organize layers by responsibility (base, reference, operational,
    selection, editing, temporary).
-   Give layers stable identities.
-   Prefer toggling visibility over repeatedly adding and removing
    layers.
-   Use `zIndex` consistently.
-   Keep transient graphics in dedicated temporary layers.

## Sources

-   Reuse sources whenever practical.
-   Batch feature additions and removals.
-   Avoid recreating sources during normal interaction.
-   Select loading strategies appropriate to dataset size.
-   Refresh only when underlying data changes.

## Features

-   Assign stable feature IDs.
-   Store only rendering-related metadata on features.
-   Keep business objects separate from OpenLayers features.
-   Update existing features rather than recreating them where
    practical.
-   Remove unused features promptly.

## Styling

-   Reuse `Style`, `Fill`, `Stroke`, `Text`, `Icon`, and `CircleStyle`
    instances.
-   Cache styles by feature type and state.
-   Avoid allocating new objects inside style functions.
-   Keep style functions deterministic.
-   Use resolution-aware styling where appropriate.
-   Keep styling logic separate from business logic.
-   Use decluttering where labels may overlap.

## Interactions

-   Enable only the interactions required for the active tool.
-   Remove or disable temporary interactions when finished.
-   Avoid overlapping editing modes.
-   Keep interaction ownership centralized.
-   Use dedicated editing workflows for draw, modify, translate, and
    snap.

## Events

-   Keep event handlers lightweight.
-   Debounce or throttle expensive operations.
-   Avoid heavy processing during `pointermove`.
-   Do not use render events for business logic.
-   Remove listeners during cleanup.

## Coordinates

-   Define a canonical application coordinate reference system (CRS).
-   Convert coordinates only at application boundaries.
-   Avoid mixing projections within the same workflow.
-   Validate projection assumptions when importing external data.

## Performance

-   Avoid recreating maps, layers, sources, and styles.
-   Prefer incremental updates over complete rebuilds.
-   Cluster dense point datasets where appropriate.
-   Consider vector tiles for very large datasets.
-   Consider WebGL rendering when Canvas performance becomes a
    bottleneck.
-   Profile before optimizing.

## Code Organization

-   Encapsulate OpenLayers behind project-specific APIs.
-   Isolate configuration from implementation.
-   Prefer explicit imports from `ol/...`.
-   Keep utility functions pure.
-   Document project conventions for layers, styles, and interactions.

## Anti-patterns

Avoid:

-   Recreating style objects during every render.
-   Searching every feature on every user interaction.
-   Mixing business state with rendering state.
-   Frequently destroying and recreating layers or sources.
-   Mixing coordinate systems without explicit conversion.
-   Allowing multiple tools to modify the same feature simultaneously.

## Decision Guide

  Scenario                                 Preferred Approach
  ---------------------------------------- ------------------------------------------
  Small to medium dynamic datasets         `VectorSource`
  Very large mostly-static datasets        Vector tiles
  Frequently changing feature appearance   Cached style functions
  Temporary graphics                       Dedicated temporary layer
  Feature selection                        Dedicated selection layer
  Interactive editing                      Dedicated editing layer and interactions

## Goals

-   Predictable architecture.
-   High rendering performance.
-   Clear separation of concerns.
-   Consistent coding conventions.
-   Straightforward migration to future OpenLayers releases.
